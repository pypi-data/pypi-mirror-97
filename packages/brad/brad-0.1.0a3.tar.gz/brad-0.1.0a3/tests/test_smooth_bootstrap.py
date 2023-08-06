import numpy as np
import pytest

from brad import smooth_bootstrap
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x5, safe_mean

KERNELS = [
    "gaussian",
    "tophat",
]
KERNELS_WITHOUT_SAMPLE = ["epanechnikov", "exponential", "linear", "cosine"]


@pytest.mark.parametrize("n_samples", [2, 7, 102])
@pytest.mark.parametrize("kernel", KERNELS)
@pytest.mark.parametrize("bandwidth", [0.1, 0.2, 0.5])
def test_shape(n_samples, kernel, bandwidth):
    data = RANDOM_10x5
    shape = data.shape

    assert (
        smooth_bootstrap(
            data, n_samples, kernel=kernel, bandwidth=bandwidth
        ).samples.shape
        == (n_samples,) + shape
    )

    assert (
        smooth_bootstrap(
            data,
            n_samples,
            kernel=kernel,
            bandwidth=bandwidth,
            statistic=safe_mean,
        ).samples.shape
        == (n_samples,)
    )


@pytest.mark.parametrize("kernel", KERNELS_WITHOUT_SAMPLE)
def test_sklearn_kernal_no_sample(kernel):
    """
    Smooth bootstrap uses scikit-learn's KDE implementation, but requires that
    we can draw samples, and this is not possible for many of the available
    kernels. Raise an error if a choice is made that does not allow samples to
    be drawn.
    """
    data = RANDOM_10x5

    with pytest.raises(ValueError):
        smooth_bootstrap(data, 1, kernel=kernel)


def test_invalid_kernel():
    data = RANDOM_10x5

    with pytest.raises(ValueError):
        smooth_bootstrap(data, 1, kernel="invalid-kernel")


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_empty_dataset(n_samples):
    empty_dataset = np.arange(0)

    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        smooth_bootstrap(empty_dataset, n_samples)


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_scalar_dataset(n_samples):
    scalar_dataset = np.array(0)

    with pytest.raises(
        ValueError, match="Parameter 'data' cannot be a scalar"
    ):
        smooth_bootstrap(scalar_dataset, n_samples)
