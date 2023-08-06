import functools
from typing import Callable, Type, TypeVar

import numpy as np
from numpy.core.numeric import asanyarray

from brad.results import (
    BootstrapDistribution,
    Distribution,
    PermutationDistribution,
)
from brad.samplers import (
    BootknifeSampler,
    JackknifeSampler,
    NonParametricSampler,
    ParametricSampler,
    PermutationSampler,
    Sampler,
    SmoothSampler,
)

T = TypeVar("T", bound=Distribution)


def _resample(
    sampler: Sampler,
    n_samples: int,
    return_type: Type[T],
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> T:
    """
    Draw `n_samples` from `sampler` and optionally apply `statistic` to each
    sample. Used as a building block for all other resampling functions.

    Args:
        n_samples: The number of samples to draw.
        sampler: A sampler from which samples will be drawn.
        statistic: A statistic that can be applied to each sample. It not
            provided, then samples are returned untouched.

    Returns:
        Data and resamples from the sampler.
    """
    statistic = statistic if statistic is not None else (lambda sample: sample)

    observation = statistic(sampler._data)

    if not isinstance(observation, float):
        observation = asanyarray(observation)

    # calculating statistic shape on the samples is necessary because they can
    # have different shape to the original data in the case of the jackknife
    sample_iterator = iter(sampler)
    sample = next(sample_iterator)
    replication = asanyarray(statistic(sample))

    statistic_shape = replication.shape

    replications = np.zeros((n_samples,) + statistic_shape)
    replications[0] = replication

    for i, sample in enumerate(sample_iterator, start=1):
        if i >= n_samples:
            break
        replications[i] = asanyarray(statistic(sample))

    return return_type(observation, replications)


def bootstrap(
    data: np.ndarray,
    n_samples: int,
    *,
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> BootstrapDistribution:
    """
    Generate bootstrap samples from data.

    Args:
        data: Input data from which to draw bootstrap samples.
        n_samples: The number of samples to draw.
        statistic: A function/statistic to apply to each bootstrap sample. If
            statistic is supplied then the returned array will have shape
            `(n_samples, ) + statistic_shape`.

    Returns:
        Data and non-parametric bootstrap resamples.
    """
    sampler = NonParametricSampler(data)
    return _resample(
        sampler, n_samples, BootstrapDistribution, statistic=statistic
    )


def smooth_bootstrap(
    data: np.ndarray,
    n_samples: int,
    *,
    kernel: str = "gaussian",
    bandwidth: float = 0.2,
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> BootstrapDistribution:
    """
    Generate smooth bootstrap samples from data. First fits a KDE to the
    provided data, then samples from the fitted smooth approximation.

    Args:
        data: Input data to which a KDE will be fit.
        n_samples: The number of sampels to draw.
        kernel: Kernel to use when fitting the KDE. Can choose
            either 'gaussian' or 'tophat'.
        bandwidth: Bandwidth of the kernel used in the KDE.
        statistic: A function/statistic to apply to each bootstrap
            sample. If statistic is supplied then the returned array will have
            shape `(n_samples, ) + statistic_shape`.

    Returns:
        Data and smooth bootstrap resamples.
    """
    sampler = SmoothSampler(data, kernel=kernel, bandwidth=bandwidth)
    return _resample(
        sampler, n_samples, BootstrapDistribution, statistic=statistic
    )


def parametric_bootstrap(
    data: np.ndarray,
    n_samples: int,
    *,
    family: str,
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> BootstrapDistribution:
    """
    Generate parametric bootstrap samples from data. First fits a parametric
    distribution to the provided data, then samples from the fitted parametric
    approximation.

    Args:
        data: Input data to which a KDE will be fit.
        n_samples: The number of sampels to draw.
        family: The parametric family from which to select the
            approximation. Options are: beta, chi2, expon, f, gamma, lognorm,
            norm, t.
        statistic: A function/statistic to apply to each bootstrap
            sample. If statistic is supplied then the returned array will have
            shape `(n_samples, ) + statistic_shape`.

    Returns:
        Data and smooth bootstrap resamples.
    """
    sampler = ParametricSampler(data, family=family)
    return _resample(
        sampler, n_samples, BootstrapDistribution, statistic=statistic
    )


def permutation_test(
    data: np.ndarray,
    labels: np.ndarray,
    n_samples: int,
    *,
    statistic: Callable[[np.ndarray, np.ndarray], np.ndarray] = None,
) -> PermutationDistribution:
    """
    Randomly permute labels and apply statistic n_samples times.

    Args:
        data: Input data with which to conduct permutation test.
        labels: Labels must have x.shape[0] == labels.shape[0].
        n_samples: The number of samples / permutations to draw.
        statistic: A function to apply to each bootstrap sample. The expected
            signature is `(x, labels) -> stat`.

    Returns:
        An array of samples with shape `(n_samples, ) + statistic_shape`.
    """
    if data.shape[0] != labels.shape[0]:
        raise ValueError(
            "Shape mismatch: first dimension of data and labels should be the "
            "same size."
        )

    sampler = PermutationSampler(labels)

    statistic = functools.partial(
        statistic or (lambda data, labels: labels), data
    )

    return _resample(
        sampler, n_samples, PermutationDistribution, statistic=statistic
    )


def bootknife(
    data: np.ndarray,
    n_samples: int,
    *,
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> BootstrapDistribution:
    """
    Generate bootknife samples from data.

    Args:
        data: Input data from which to draw bootstrap samples.
        n_samples: The number of samples to draw.
        statistic:
            A function/statistic to apply to each bootstrap sample. If
            statistic is supplied then the returned array will have shape
            `(n_samples, ) + statistic_shape`.

    Returns:
        An array of samples.
    """
    sampler = BootknifeSampler(data)
    return _resample(
        sampler, n_samples, BootstrapDistribution, statistic=statistic
    )


def jackknife(
    data: np.ndarray,
    *,
    statistic: Callable[[np.ndarray], np.ndarray] = None,
) -> BootstrapDistribution:
    """
    Generate jackknife samples from data.

    Args:
        data: Input data from which to draw jackknife samples.
        statistic: A function/statistic to apply to each sample. If
            statistic is supplied then the returned array will have shape
            `(n_samples, ) + statistic_shape`.

    Returns:
        An array of samples.
    """
    sampler = JackknifeSampler(data)
    # TODO: this is broken
    statistic = (
        statistic
        if statistic is not None
        else (lambda sample: sample[: sampler._data.shape[0] - 1])
    )
    return _resample(
        sampler, len(data), BootstrapDistribution, statistic=statistic
    )
