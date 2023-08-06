import abc
from typing import Iterator

import numpy as np
from numpy.core.numeric import asanyarray
from scipy.stats.distributions import (
    beta,
    chi2,
    expon,
    f,
    gamma,
    lognorm,
    norm,
    t,
)
from sklearn.neighbors import KernelDensity

from brad.exceptions import EmptyDataError

__all__ = ["NonParametricSampler", "ParametricSampler", "SmoothSampler"]

# all scipy distributions have loc and scale parameters that allow you to
# shift and stretch the distributions. For now, we force loc and scale to
# be 0 and 1 resp. so that standard versions of the distributions are fit
_DIST_LOOKUP = {
    "beta": [beta, {"floc": 0, "fscale": 1}],
    "chi2": [chi2, {"floc": 0, "fscale": 1}],
    "expon": [expon, {"fscale": 1}],
    "f": [f, {"floc": 0, "fscale": 1}],
    "gamma": [gamma, {"floc": 0}],
    "lognorm": [lognorm, {"fscale": 1}],
    "norm": [norm, {}],
    "t": [t, {"floc": 0, "fscale": 1}],
}


class Sampler(abc.ABC):
    """
    Sampler base class. Samplers generate samples from a data set with their
    __iter__ method. They should be able to yield samples indefinitely, things
    like the sample_size are controlled at a higher level (hopefully to make
    parallelisation easier).
    """

    def __init__(self, data: np.ndarray) -> None:
        """
        Args:
            data: Dataset to draw samples from. Samples are taken along the
                zeroth dimension.
        """
        self._data = asanyarray(data)

        if self._data.ndim == 0:
            raise ValueError("Parameter 'data' cannot be a scalar")
        elif self._data.size == 0:
            raise EmptyDataError("Supplied data is empty! Nothing to sample")

        self.sample_size = self._data.shape[0]

    @abc.abstractclassmethod
    def __iter__(self) -> Iterator[np.ndarray]:
        """This method should yield samples from the sampler"""


class NonParametricSampler(Sampler):
    """
    Constructs samples by sampling the original dataset with replacement. Used
    for computing the non-parametric bootstrap.
    """

    def __init__(
        self, data: np.ndarray, *, max_buffer: int = 1_000_000
    ) -> None:
        """
        Args:
            data: Dataset to draw samples from. Samples are taken along the
                zeroth dimension.
            max_buffer: Indices for resampling are sampled in large batches and
                stored in a buffer for efficiency. This argument sets the size
                of that buffer.
        """
        super().__init__(data)
        self.max_buffer = max(max_buffer, self.sample_size)

    def __iter__(self) -> Iterator[np.ndarray]:
        buffer_size = self.max_buffer - (self.max_buffer % self.sample_size)

        rng = np.random.default_rng()

        while True:
            buffer = rng.choice(self.sample_size, buffer_size)

            for batch in np.split(buffer, buffer_size // self.sample_size):
                yield self._data[batch]


class ParametricSampler(Sampler):
    """
    Fits a parametric approximation to the data, then draws samples from the
    approximation. Used for computing the parametric bootstrap.
    """

    def __init__(self, data: np.ndarray, *, family: str) -> None:
        """
        Args:
            data: Dataset to fit parametric approximation to. Must be 1-dimensional.
            family: Parametric family to fit data to. Options are: `beta`,
                `chi2`, `expon`, `f`, `gamma`, `lognorm`, `norm`, `t`.
        """
        super().__init__(data)

        if self._data.ndim != 1:
            raise ValueError("Parametric samplers expect 1-d data.")

        if family in _DIST_LOOKUP:
            self._dist, self._fit_kwargs = _DIST_LOOKUP[family]
        else:
            raise ValueError(
                f"Invalid option '{family}' for parameter 'family'"
            )

        self._args = self._dist.fit(self._data, **self._fit_kwargs)

    def __iter__(self) -> Iterator[np.ndarray]:
        while True:
            yield self._dist.rvs(*self._args, size=self.sample_size)


class SmoothSampler(Sampler):
    """
    Fits a kernel density estimator to the data, then draws samples from the
    approximation. Used for computing the smooth bootstrap.
    """

    def __init__(
        self,
        data: np.ndarray,
        *,
        kernel: str = "gaussian",
        bandwidth: float = 0.2,
    ) -> None:
        """
        Args:
            data: Dataset to fit smooth approximation to.
            kernel: Kernel to use in the KDE. Options are `gaussian` or
                `tophat`.
            bandwidth: Bandwidth of the KDE.
        """
        if kernel not in {"gaussian", "tophat"}:
            raise ValueError(
                f"Invalid option '{kernel}' for parameter 'kernel'"
            )

        super().__init__(data)
        self.kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(
            self._data
        )

    def __iter__(self) -> Iterator[np.ndarray]:
        while True:
            yield self.kde.sample(n_samples=self.sample_size)


class JackknifeSampler(Sampler):
    """
    Generates samples by a leave-one-out strategy. A little different to the
    other samplers as will only yield finitely many samples.
    """

    def __iter__(self):
        for i in range(self.sample_size):
            yield np.delete(self._data, i, axis=0)


class BootknifeSampler(Sampler):
    """
    Generates samples by leaving out one datapoint, then sampling with
    replacement N times from the remaining N - 1 datapoints. Used for
    calculating bootknife estimates, which are similar to non-parametric
    bootstrap estimates, but with reduced bias.

    Bootknife sees best results with stratified samples (i.e. when each
    datapoint is left out equally often, or approximately so if the number of
    samples is not a multiple of the number of datapoints). This sampler does
    a stratification like this, but randomises the order of the datapoints so
    that there isn't a systematic bias toward the early datapoints should
    multiple samplers be created and their samples combined.
    """

    def __init__(self, data: np.ndarray, *, max_buffer=1_000_000) -> None:
        """
        Args:
            data: Dataset to draw samples from. Samples are taken along the
                zeroth dimension.
            max_buffer: Indices for resampling are sampled in large batches and
                stored in a buffer for efficiency. This argument sets the size
                of that buffer.
        """
        super().__init__(data)
        self.max_buffer = max_buffer

    def __iter__(self) -> Iterator[np.ndarray]:
        buffer_size = self.max_buffer - (self.max_buffer % self.sample_size)

        rng = np.random.default_rng()

        # to ensure good stratification we randomise the order of the features
        # then delete them in order. stratification will be imperfect when done
        # in parallel by multiple workers, but it will be pretty good.
        order = rng.permutation(self.sample_size)
        idx = 0

        while True:
            buffer = rng.choice(self.sample_size - 1, buffer_size)

            for batch in np.split(buffer, buffer_size // self.sample_size):
                yield np.delete(self._data, order[idx], axis=0)[batch]
                idx = (idx + 1) % self.sample_size


class PermutationSampler(Sampler):
    """
    Generates samples by a permuting the dataset. Used to conduct permutation
    tests by sampling permutations of the labels in a labelled dataset.
    """

    def __iter__(self) -> Iterator[np.ndarray]:
        rng = np.random.default_rng()

        while True:
            yield self._data[rng.permutation(self.sample_size)]
