import numpy as np
import pytest

from brad import permutation_test
from brad.exceptions import EmptyDataError

from .helpers import safe_mean

RANDOM_LABELS = np.random.binomial(1, 0.5, size=(20,))
RANDOM_DATA = np.random.normal(RANDOM_LABELS)
LABELS = np.array([1, 2, 4, 125, 1261, 0.1])


def mean_diff(x, y):
    return safe_mean(x[y == 1]) - safe_mean(x[y == 0])


def make_check_permutation(labels):
    def check_permutation(_, y):
        return set(labels[~np.isnan(labels)].tolist()) == set(
            y[~np.isnan(y)].tolist()
        )

    return check_permutation


def test_shape():
    for n in [2, 7, 102]:
        result = permutation_test(
            RANDOM_DATA, RANDOM_LABELS, n, statistic=mean_diff
        )
        assert result.samples.shape == (n,)


def test_empty_dataset():
    for n in [2, 7, 102]:
        empty_dataset = np.arange(0)
        check_permutation = make_check_permutation(empty_dataset)
        with pytest.raises(
            EmptyDataError, match="Supplied data is empty! Nothing to sample"
        ):
            permutation_test(
                empty_dataset, empty_dataset, n, statistic=check_permutation
            )


def test_permutation_test_samples_lables_permutations():
    check_permutation = make_check_permutation(LABELS)
    result = permutation_test(
        np.arange(6), LABELS, 1000, statistic=check_permutation
    )
    assert result.samples.all()


def test_data_labels_mismatch():
    with pytest.raises(ValueError):
        permutation_test(np.arange(10), np.arange(11), 10)
