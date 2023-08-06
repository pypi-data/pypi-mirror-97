import numpy as np
import pytest

from brad import bootknife
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x5, safe_mean

TUPLES = ((1, 2), (1, 6), (4, 7))
TUPLES_SET = set(TUPLES)


@pytest.mark.parametrize("n_samples", [2, 7, 102])
def test_shape(n_samples):
    data = RANDOM_10x5
    shape = data.shape

    assert bootknife(data, n_samples).samples.shape == (n_samples,) + shape
    assert bootknife(data, n_samples, statistic=safe_mean).samples.shape == (
        n_samples,
    )


def test_bootknife_empty_dataset():
    empty_dataset = np.arange(0)

    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        bootknife(empty_dataset, 1)


def test_bootknife_scalar_dataset():
    scalar_dataset = np.array(0)

    with pytest.raises(
        ValueError, match="Parameter 'data' cannot be a scalar"
    ):
        bootknife(scalar_dataset, 1)


def test_bootknife_returned_values_are_samples():
    samples = bootknife(TUPLES, 10).samples
    assert all(
        [
            tuple(samples[i, j]) in TUPLES_SET
            for i in range(10)
            for j in range(3)
        ]
    )
