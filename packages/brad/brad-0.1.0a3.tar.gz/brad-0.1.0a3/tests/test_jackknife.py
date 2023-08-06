import numpy as np
import pytest

from brad import jackknife
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x5, safe_mean

TUPLES = ((1, 2), (1, 6), (4, 7))
TUPLES_SET = set(TUPLES)


def test_shape():
    shape = RANDOM_10x5.shape

    assert (
        jackknife(RANDOM_10x5).samples.shape
        == (shape[0], shape[0] - 1) + shape[1:]
    )
    assert jackknife(RANDOM_10x5, statistic=safe_mean).samples.shape == (
        shape[0],
    )


def test_bootknife_empty_dataset():
    empty_dataset = np.arange(0)
    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        jackknife(empty_dataset)


def test_bootknife_returned_values_are_samples():
    samples = jackknife(TUPLES).samples
    assert all(
        [
            tuple(samples[i, j]) in TUPLES_SET
            for i in range(3)
            for j in range(2)
        ]
    )
