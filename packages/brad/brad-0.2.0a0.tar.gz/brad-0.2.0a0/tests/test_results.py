import numpy as np
import pytest

from brad.results import (
    BootstrapDistribution,
    ConfidenceInterval,
    PermutationDistribution,
)

from .helpers import RANDOM_10x1


def test_standard_error():
    bootstrap_dist = BootstrapDistribution(2.0, np.arange(5))

    assert np.isclose(bootstrap_dist.standard_error(), np.sqrt(2.5))
    assert np.isclose(bootstrap_dist.standard_error(ddof=0), np.sqrt(2))


def test_standard_error_1d_check():
    bootstrap_dist_non_scalar_data = BootstrapDistribution(
        np.zeros(3), np.zeros(3)
    )

    with pytest.raises(ValueError):
        bootstrap_dist_non_scalar_data.standard_error()

    bootstrap_dist_2d_samples = BootstrapDistribution(0.0, np.zeros((2, 2)))

    with pytest.raises(ValueError):
        bootstrap_dist_2d_samples.standard_error()


@pytest.mark.parametrize("confidence_level", [0.9, 0.95, 0.99])
@pytest.mark.parametrize("kind", ["pivotal", "normal", "percentile"])
def test_confidence_interval(confidence_level, kind):
    bootstrap_dist = BootstrapDistribution(0.0, RANDOM_10x1)

    ci = bootstrap_dist.confidence_interval(
        confidence_level=confidence_level, kind=kind
    )

    assert isinstance(ci, ConfidenceInterval)
    assert ci.kind == kind
    assert ci.confidence_level == confidence_level


def test_confidence_interval_1d_check():
    bootstrap_dist_non_scalar_data = BootstrapDistribution(
        np.zeros(3), np.zeros(3)
    )

    with pytest.raises(ValueError):
        bootstrap_dist_non_scalar_data.confidence_interval()

    bootstrap_dist_2d_samples = BootstrapDistribution(0.0, np.zeros((2, 2)))

    with pytest.raises(ValueError):
        bootstrap_dist_2d_samples.confidence_interval()


def test_confidence_interval_kind():
    bootstrap_dist = BootstrapDistribution(0.0, RANDOM_10x1)

    with pytest.raises(ValueError):
        bootstrap_dist.confidence_interval(kind="snorf")


def test_p_value():
    permutation_dist = PermutationDistribution(3.4, np.arange(5))

    assert permutation_dist.p_value() == 0.2
    assert permutation_dist.p_value(lower_tail=True) == 0.8


def test_p_value_1d_check():
    permutation_dist_non_scalar_data = PermutationDistribution(
        np.zeros(3), np.zeros(3)
    )

    with pytest.raises(ValueError):
        permutation_dist_non_scalar_data.p_value()

    permutation_dist_2d_samples = PermutationDistribution(
        0.0, np.zeros((2, 2))
    )

    with pytest.raises(ValueError):
        permutation_dist_2d_samples.p_value()
