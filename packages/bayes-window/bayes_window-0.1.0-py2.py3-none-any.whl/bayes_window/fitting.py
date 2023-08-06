import arviz as az
import numpyro
from jax import random
from numpyro.infer import MCMC, NUTS

from . import models


def fit_numpyro(progress_bar=False, model=None, n_draws=1000, num_chains=1, convert_to_arviz=True, **kwargs):
    model = model or models.model_hierarchical
    numpyro.set_host_device_count(4)
    mcmc = MCMC(NUTS(model), num_warmup=1000, num_samples=n_draws, num_chains=num_chains, progress_bar=progress_bar)
    mcmc.run(random.PRNGKey(16), **kwargs)

    # arviz convert
    trace = az.from_numpyro(mcmc)
    # Print diagnostics
    if trace.sample_stats.diverging.sum(['chain', 'draw']).values > 0:
        print(f"n(Divergences) = {trace.sample_stats.diverging.sum(['chain', 'draw']).values}")
    if convert_to_arviz:
        return trace
    else:
        return mcmc
