import numpy as np
import pytest

from brad import bootstrap
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x5, safe_mean

TUPLES = ((1, 2), (1, 6), (4, 7))
TUPLES_SET = set(TUPLES)
TUPLES_SET_T = {(1, 1, 4), (2, 6, 7)}


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_shape(n_samples):
    data = RANDOM_10x5
    shape = data.shape

    assert bootstrap(data, n_samples).samples.shape == (n_samples,) + shape
    assert bootstrap(data, n_samples, statistic=safe_mean).samples.shape == (
        n_samples,
    )


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_empty_dataset(n_samples):
    empty_dataset = np.arange(0)

    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        bootstrap(empty_dataset, n_samples)


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_scalar_dataset(n_samples):
    scalar_dataset = np.array(0)

    with pytest.raises(
        ValueError, match="Parameter 'data' cannot be a scalar"
    ):
        bootstrap(scalar_dataset, n_samples)


def test_returned_values_are_samples():
    n_samples = 5
    samples = bootstrap(TUPLES, n_samples).samples
    assert all(
        [
            tuple(samples[i, j]) in TUPLES_SET
            for i in range(n_samples)
            for j in range(3)
        ]
    )
