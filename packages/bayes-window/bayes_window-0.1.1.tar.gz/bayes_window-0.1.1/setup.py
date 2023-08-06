#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ['pytest-runner', 'joblib', 'numpy', 'numpyro', 'bulwark', 'elephant', 'xarray', 'altair',
                      # 'jax',
                      # 'jaxlib==0.1.51',
                      'pandas', 'arviz', 'sklearn', 'inflection','nbsphinx','nbval','statsmodels']

test_requirements = ['pytest>=3', ]

setup(
    author="Maxym Myroshnychenko",
    author_email='mmyros@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Pretty and easy Bayesian estimation with data overlay",
    entry_points={
        'console_scripts': [
            'bayes_window=bayes_window.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bayes_window',
    name='bayes_window',
    packages=find_packages(include=['bayes_window', 'bayes_window.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mmyros/bayes_window',
    version='0.1.1',
    zip_safe=False,
)
