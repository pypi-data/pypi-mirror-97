import numpy as np
import pytest

from brad.models import ConfidenceInterval, Resample

from .helpers import RANDOM_10x1


def test_standard_error():
    resample = Resample(2.0, np.arange(5))

    assert np.isclose(resample.standard_error(), np.sqrt(2.5))
    assert np.isclose(resample.standard_error(ddof=0), np.sqrt(2))


def test_standard_error_1d_check():
    resample_non_scalar_data = Resample(np.zeros(3), np.zeros(3))

    with pytest.raises(ValueError):
        resample_non_scalar_data.standard_error()

    resample_2d_samples = Resample(0.0, np.zeros((2, 2)))

    with pytest.raises(ValueError):
        resample_2d_samples.standard_error()


@pytest.mark.parametrize("confidence_level", [0.9, 0.95, 0.99])
@pytest.mark.parametrize("kind", ["pivotal", "normal", "percentile"])
def test_confidence_interval(confidence_level, kind):
    resample = Resample(0.0, RANDOM_10x1)

    ci = resample.confidence_interval(
        confidence_level=confidence_level, kind=kind
    )

    assert isinstance(ci, ConfidenceInterval)
    assert ci.kind == kind
    assert ci.confidence_level == confidence_level


def test_confidence_interval_1d_check():
    resample_non_scalar_data = Resample(np.zeros(3), np.zeros(3))

    with pytest.raises(ValueError):
        resample_non_scalar_data.confidence_interval()

    resample_2d_samples = Resample(0.0, np.zeros((2, 2)))

    with pytest.raises(ValueError):
        resample_2d_samples.confidence_interval()


def test_confidence_interval_kind():
    resample = Resample(0.0, RANDOM_10x1)

    with pytest.raises(ValueError):
        resample.confidence_interval(kind="snorf")
