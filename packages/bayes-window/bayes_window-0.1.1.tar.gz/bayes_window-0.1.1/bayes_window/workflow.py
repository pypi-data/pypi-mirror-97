import warnings
from importlib import reload

import altair as alt
import numpy as np
import pandas as pd
import statsmodels.formula.api as sm
from sklearn.preprocessing import LabelEncoder

from bayes_window import models
from bayes_window import utils
from bayes_window import visualization
from bayes_window.fitting import fit_numpyro
from bayes_window.model_comparison import compare_models
from bayes_window.visualization import plot_posterior

reload(visualization)
le = LabelEncoder()


def combined_condition(df, levels):
    # String-valued combined condition
    # df['combined_condition'] = utils.df_index_compress(df, index_columns=self.levels)[1]
    df['combined_condition'] = df[levels[0]].astype('str')
    for level in levels[1:]:
        df['combined_condition'] += df[level].astype('str')
    data = df.copy()
    # Transform conditions to integers as required by numpyro:
    data['combined_condition'] = le.fit_transform(df['combined_condition'])
    # Transform conditions to integers as required by numpyro:
    key = dict()
    for level in levels:
        data[level] = le.fit_transform(data[level])
        # Keep key for later use
        # TODO I don't think this key is currently used for plotting, is it? Test with mouse names
        key[level] = dict(zip(range(len(le.classes_)), le.classes_))
    return data, key


class BayesWindow:
    def __init__(self,
                 df: pd.DataFrame,
                 y: str,
                 treatment: str,
                 condition: str or list = None,
                 group: str = None,
                 detail=':O'
                 ):
        assert y in df.columns
        assert treatment in df.columns
        if group:
            assert group in df.columns
        self.treatment = treatment  # if type(treatment)=='list' else [treatment]  # self.levels[2]
        self.group = group  # if type(group)=='list' else [group] # self.levels[1]  # Eg subject
        self.condition = condition if type(condition) == list else [condition]
        if self.condition[0]:
            assert self.condition[0] in df.columns
        self.levels = utils.parse_levels(self.treatment, self.condition, self.group)
        self.data, self._key = combined_condition(df, self.levels)
        self.detail = detail
        self.y = y

        # Preallocate attributes:
        self.b_name = None  # Depends on model we'll fit
        self.do_make_change = None  # Depends on plotting input
        self.add_data = None  # We'll use this in plotting
        self.independent_axes = None
        self.data_and_posterior = None
        self.posterior = None
        self.trace = None
        self.model = None

    def fit_anova(self):
        from statsmodels.stats.anova import anova_lm
        if self.group:
            # Average over group:
            data = self.data.groupby([self.group, self.treatment]).mean().reset_index()
        else:
            data = self.data
        # dehumanize all columns and variable names for statsmodels:
        [data.rename({col: col.replace(" ", "_")}, axis=1, inplace=True) for col in data.columns]
        self.y = self.y.replace(" ", "_")
        formula = f'{self.y}~{self.treatment}'
        lm = sm.ols(formula, data=data).fit()
        print(f'{formula}\n {anova_lm(lm, typ=2)}')
        return anova_lm(lm, typ=2)['PR(>F)'][self.treatment] < 0.05

    def fit_lme(self, add_data=False, do_make_change='divide'):
        # model = MixedLM(endog=self.data[self.y],
        #                 exog=self.data[self.condition],
        #                 groups=self.data[self.group],
        #                 # exog_re=exog.iloc[:, 0]
        #                 )
        # dehumanize all columns and variable names for statsmodels:
        [self.data.rename({col: col.replace(" ", "_")}, axis=1, inplace=True) for col in self.data.columns]
        self.y = self.y.replace(" ", "_")
        self.group = self.group.replace(" ", "_")
        self.treatment = self.treatment.replace(" ", "_")
        self.do_make_change = do_make_change
        include_condition = False
        if self.condition[0]:
            if len(self.data[self.condition[0]].unique()) > 1:
                include_condition = True
        if include_condition:
            if len(self.condition) > 1:
                raise NotImplementedError(f'conditions {self.condition}')
                # This would need a combined condition dummy variable and an index of condition in patsy:
                # formula = f"{self.y} ~ 1+ {self.condition}(condition_index) | {self.treatment}"
            self.condition[0] = self.condition[0].replace(" ", "_")
            formula = f"{self.y} ~ 1+ {self.condition[0]} | {self.treatment}"
        else:
            formula = f"{self.y} ~ 1 + {self.treatment}"
        if self.group:
            formula += f' + (1 | {self.group})'
        print(f'Using formula {formula}')
        result = sm.mixedlm(formula,
                            self.data,
                            groups=self.data[self.group]).fit()
        res = result.summary().tables[1]
        res = res.iloc[:-1]
        try:
            res = res.astype(float)  # [['P>|z|', 'Coef.', '[0.025', '0.975]']]
        except Exception as e:
            warnings.warn(f'somehow LME failed to estimate CIs for one or more variables. Replacing with nan:'
                          f' {e} \n=>\n {res}')
            res.replace({'': np.nan}).astype(float)
        res = res.rename({'P>|z|': 'p',
                          'Coef.': 'center interval',
                          '[0.025': 'higher interval',
                          '0.975]': 'lower interval'}, axis=1)
        self.posterior = res
        if add_data and self.condition[0]:
                raise NotImplementedError("I don't understand if there is a way to get separate estimates "
                                          "of slope per condition in LME, or do you just get an effect size estimate??")
                # like in hdi2df:
                from utils import fill_row
                rows = [fill_row(group_val, rows, res, group_name=self.condition[0])
                        for group_val, rows in self.data.groupby([self.condition[0]])
                        ]
                self.data_and_posterior = pd.concat(rows)
        elif add_data:
            # like in hdi2df_one_condition():
            self.data_and_posterior = self.data.copy()
            for col in ['lower interval', 'higher interval', 'center interval']:
                self.data_and_posterior.insert(self.data.shape[1],
                                               col,
                                               res.loc[self.treatment, col])

        return self

    def fit_conditions(self, model=models.model_single, add_data=True):

        self.model = model
        self.b_name = 'mu_per_condition'
        # Estimate model
        self.trace = fit_numpyro(y=self.data[self.y].values,
                                 condition=self.data['combined_condition'].values,
                                 model=model,
                                 ).posterior

        # Add data back
        if add_data:
            self.data_and_posterior, self.trace = utils.add_data_to_posterior(df_data=self.data,
                                                                              posterior=self.trace,
                                                                              y=self.y,
                                                                              fold_change_index_cols=self.levels[:3],
                                                                              treatment_name=self.levels[0],
                                                                              b_name=self.b_name,
                                                                              posterior_index_name='combined_condition',
                                                                              do_mean_over_trials=False,
                                                                              do_make_change=False,
                                                                              add_data=add_data
                                                                              )
        return self

    def fit_slopes(self, model=models.model_hierarchical, do_make_change='subtract',
                   fold_change_index_cols=None, do_mean_over_trials=True, add_data: bool = True, **kwargs):
        # TODO case with no group_name
        if do_make_change not in ['subtract', 'divide']:
            raise ValueError(f'do_make_change should be subtract or divide, not {do_make_change}')

        self.b_name = 'b_stim_per_condition'
        self.do_make_change = do_make_change
        self.add_data = add_data  # We'll use this in plotting
        self.model = model
        # TODO handle no-group case
        if fold_change_index_cols is None:
            # TODO case with no plot_index_cols should include any multiindex?
            fold_change_index_cols = self.levels  # [-1]
        if not self.condition[0]:
            warnings.warn('Condition was not provided. Assuming there is no additional condition, just treatment')
            self.condition[0] = 'dummy_condition'
            self.data.insert(self.data.shape[-1] - 1, 'dummy_condition', np.ones(self.data.shape[0]))
            fold_change_index_cols.append('dummy_condition')
        if not self.condition[0] in fold_change_index_cols:
            fold_change_index_cols.extend(self.condition)
        try:
            self.trace = fit_numpyro(y=self.data[self.y].values,
                                     treatment=self.data[self.treatment].values,
                                     condition=self.data[self.condition[0]].values,
                                     group=self.data[self.group].values,
                                     progress_bar=False,
                                     model=model,
                                     n_draws=1000, num_chains=1,
                                     **kwargs)
        except TypeError as e:
            # assert that model() has kwarg stim, because this is slopes
            raise KeyError(f'Does your model {model} have "stim" argument? You asked for slopes!{e}')
        if add_data:
            # Add data back
            # TODO posterior_index_name=self.condition[0] will not work if need combined_condition
            df_result, self.trace.posterior = utils.add_data_to_posterior(df_data=self.data,
                                                                          posterior=self.trace.posterior,
                                                                          y=self.y,
                                                                          fold_change_index_cols=fold_change_index_cols,
                                                                          treatment_name=self.treatment,
                                                                          b_name=self.b_name,
                                                                          posterior_index_name=self.condition[0],
                                                                          do_make_change=do_make_change,
                                                                          do_mean_over_trials=do_mean_over_trials,
                                                                          add_data=self.add_data
                                                                          )
        else:  # Just convert posterior to dataframe
            from bayes_window.utils import trace2df
            # TODO we add data regardless. Is there a way to not use self.data?
            df_result, self.trace.posterior = trace2df(self.trace.posterior,
                                                       self.data, b_name=self.b_name,
                                                       posterior_index_name=self.condition[0])

        # Back to human-readable labels
        [df_result[col].replace(self._key[col], inplace=True) for col in self._key.keys()
         if (not col == self.treatment) and (col in df_result)]
        self.data_and_posterior = df_result
        return self

    def plot_posteriors_slopes(self, x=':O', color=':O', add_box=True, independent_axes=False, **kwargs):
        # Set some options
        self.independent_axes = independent_axes
        x = x or self.levels[-1]
        if x[-2] != ':':
            x += ':O'
        color = color or self.levels[0]

        # Plot posterior
        if self.data_and_posterior is not None:
            add_data = self.add_data
            base_chart = alt.Chart(self.data_and_posterior)
            chart_p = plot_posterior(title=f'{self.y}',
                                     x=x,
                                     base_chart=base_chart,
                                     do_make_change=self.do_make_change)
        else:
            base_chart = alt.Chart(self.data)
            add_data = True  # Otherwise nothing to do

        if add_data:
            assert self.data_and_posterior is not None
            chart_d = visualization.plot_data(x=x, y=f'{self.y} diff', color=color, add_box=add_box,
                                              base_chart=base_chart)
            self.chart = chart_d + chart_p
        else:
            self.chart = chart_p
        if independent_axes:
            self.chart = self.chart.resolve_scale(y='independent')
        return self.chart

    # TODO plot_posteriors_slopes and plot_posteriors_no_slope can be one
    def plot_posteriors_no_slope(self,
                                 x=None,
                                 add_data=False,
                                 independent_axes=True,
                                 color=None,
                                 detail=':O',
                                 **kwargs):
        self.independent_axes = independent_axes
        x = x or self.treatment
        detail = detail or self.detail
        color = color or self.condition[0]
        # TODO default for detail
        if self.data_and_posterior is not None:
            base_chart = alt.Chart(self.data_and_posterior)
            # Plot posterior
            chart_p = visualization.plot_posterior(x=x,
                                                   do_make_change=False,
                                                   add_data=add_data,
                                                   # title=f'{self.y} estimate', #TODO uncomment
                                                   base_chart=base_chart,
                                                   **kwargs
                                                   )
            if not add_data:  # done
                self.chart = chart_p
        else:
            add_data = True  # Otherwise nothing to do
            base_chart = alt.Chart(self.data)

        if add_data:
            # Make data plot:
            chart_d = visualization.plot_data_slope_trials(x=x,
                                                           y=self.y,
                                                           color=color,
                                                           detail=detail,
                                                           base_chart=base_chart)

            if self.data_and_posterior is None:
                self.chart = chart_d  # we're done
            else:
                self.chart = chart_p + chart_d

        return self.chart

    def plot(self, **kwargs):
        # Convenience function
        if not self.b_name:
            warnings.warn('No model has been fit. Defaulting to plotting "slopes" for data. Use .plot_slopes'
                          'or .plot_posteriors_no_slope to be explicit ')
            return visualization.plot_data(self.data, x=self.levels[0], y=self.y,
                                           color=self.levels[1] if len(self.levels) > 1 else None,
                                           **kwargs)

        if self.b_name == 'b_stim_per_condition':
            return BayesWindow.plot_posteriors_slopes(self, **kwargs)
        elif self.b_name == 'mu_per_condition':
            return BayesWindow.plot_posteriors_no_slope(self, **kwargs)

    def facet(self, width=50, height=60, **kwargs):
        assert ('row' in kwargs) or ('column' in kwargs), 'Give facet either row, or column'
        if self.independent_axes is None:
            # TODO let's not force users to plot. have a sensible default
            raise RuntimeError('Plot first, then you can use facet')
        if self.independent_axes:
            self.facetchart = visualization.facet(self.chart, width=width, height=height, **kwargs)
        else:
            self.facetchart = self.chart.properties(width=width, height=height).facet(**kwargs)
        return self.facetchart

    def plot_model_quality(self, var_names=None):
        import arviz as az
        assert hasattr(self, 'trace'), 'Run bayesian fitting first!'
        az.plot_trace(self.trace, var_names=var_names, show=True)

    def explore_models(self, parallel=True):
        if self.b_name is None:
            raise ValueError('Fit a model first')
        elif self.b_name == 'mu_per_condition':
            return compare_models(df=self.data,
                                  models={
                                      'no_condition': self.model,
                                      'full_normal': self.model,
                                      'full_student': self.model,
                                      'full_lognogmal': self.model,
                                  },
                                  extra_model_args=[
                                      {'condition': None},
                                      {'condition': self.condition},
                                      {'condition': self.condition},
                                      {'condition': self.condition},
                                  ],
                                  y=self.y,
                                  parallel=True
                                  )

        elif self.b_name == 'b_stim_per_condition':
            return compare_models(df=self.data,
                                  models={
                                      'full_normal': self.model,
                                      'no_condition': self.model,
                                      'no_condition_or_treatment': self.model,
                                      'no-treatment': self.model,
                                      'no_group': self.model,
                                      'full_student': self.model,
                                      'full_lognogmal': self.model,
                                  },
                                  extra_model_args=[
                                      {'treatment': self.treatment, 'condition': self.condition, 'group': self.group},
                                      {'treatment': self.treatment, 'condition': None},
                                      {'treatment': None, 'condition': None},
                                      {'treatment': None, 'condition': self.condition},
                                      {'treatment': self.treatment, 'condition': self.condition, 'group': None},
                                      {'treatment': self.treatment, 'condition': self.condition, 'group': self.group,
                                       'dist_y': 'student', },
                                      {'treatment': self.treatment, 'condition': self.condition, 'group': self.group,
                                       'dist_y': 'lognormal'},
                                  ],
                                  y=self.y,
                                  parallel=parallel
                                  )
