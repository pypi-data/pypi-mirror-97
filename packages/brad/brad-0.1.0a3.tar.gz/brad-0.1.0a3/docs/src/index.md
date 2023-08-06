# Brad documentation

![gh-actions](https://github.com/tcbegley/brad/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/tcbegley/brad/branch/main/graph/badge.svg?token=aJUDsDeu1t)](https://codecov.io/gh/tcbegley/brad)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/brad)
![PyPI - License](https://img.shields.io/pypi/l/brad)

`brad` is a Python package that implements the bootstrap, permutation tests and
other resampling functions. See below for installation instructions. Also check
out the [User Guide](user-guide/) for an overview of the library, recap of the
theory behind the bootstrap, and some basic usage examples. Finally `brad`'s API
is fully documented in the [API Reference](reference/).

This library was created primarily as a means for the authors to learn more
about the bootstrap themselves, but we hope our implementations are nevertheless
useful, and that this documentation is a useful resource for those who are
learning about these methods for the first time.

## Installation

`brad` requires Python 3.7 or later, and can be installed with `pip`.

```sh
pip install -U brad
```

That's it! :tada: You can also install directly from source with

```sh
pip install -U git+https://github.com/tcbegley/brad.git
```

## Quick example

Here's a quick example. Let's suppose we have a sample from a normal
distribution.

```python
import numpy as np

rng = np.random.default_rng()
data = rng.normal(0, 2, size=50)
```

We want to estimate the standard deviation. We can do this in NumPy with
`#!python np.std(data, ddof=1)`. We will use the `bootstrap` function from
`brad` to resample `data` many times to estimate the sampling distribution.

```python
from brad import bootstrap

resample = bootstrap(
    data, n_samples=10_000, statistic=lambda x: np.std(x, ddof=1)
)
```

Here we tell `brad` to sample with replacement from `data` 10,000 times, and
apply `statistic` to each resample. The result is a `Resample` dataclass, with
which we can easily compute the bootstrap standard error

```python
resample.standard_error()
```

or confidence intervals.

```python
resample.confidence_interval(confidence_level=0.95, kind="pivotal")
```

`brad` can calculate three kinds of confidence interval: pivotal, percentile and
normal. Each of these options is specified using the `kind` keyword argument.
It's also easy to recover the statistic applied to the original data

```python
resample.data
```

or the statistic applied to each of the samples

```python
resample.samples
```
