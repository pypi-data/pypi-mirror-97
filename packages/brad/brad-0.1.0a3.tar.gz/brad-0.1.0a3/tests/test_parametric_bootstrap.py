import numpy as np
import pytest
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

from brad import parametric_bootstrap
from brad.exceptions import EmptyDataError

from .helpers import RANDOM_10x1, RANDOM_10x5, safe_mean

dist_names = [d.name for d in [lognorm, norm]]

DISTRIBUTIONS = [beta, chi2, expon, f, gamma, lognorm, norm, t]
DISTRIBUTION_PARAMETERS = [
    (3, 5),
    (5,),
    (5,),
    (50, 50),
    (6, 0, 4),
    (5, 1),
    (3, 2),
    (4,),
]
FAMILY_DATA = [
    (d.name, d.rvs(*params, size=1000))
    for d, params in zip(DISTRIBUTIONS, DISTRIBUTION_PARAMETERS)
]


# F distribution spits out a runtime warning when fitting
@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.parametrize("n_samples", [2, 7, 102])
@pytest.mark.parametrize("family,data", FAMILY_DATA)
def test_shape(n_samples, family, data):
    shape = data.shape

    assert parametric_bootstrap(
        data, n_samples, family=family
    ).samples.shape == (
        n_samples,
        shape[0],
    )
    assert parametric_bootstrap(
        data, n_samples, family=family, statistic=safe_mean
    ).samples.shape == (n_samples,)


def test_empty_dataset():
    empty_dataset = np.arange(0)

    with pytest.raises(
        EmptyDataError, match="Supplied data is empty! Nothing to sample"
    ):
        parametric_bootstrap(empty_dataset, 1, family="norm")


def test_scalar_dataset():
    scalar_dataset = np.array(0)

    with pytest.raises(
        ValueError, match="Parameter 'data' cannot be a scalar"
    ):
        parametric_bootstrap(scalar_dataset, 1, family="norm")


def test_1d_data():
    with pytest.raises(
        ValueError, match="Parametric samplers expect 1-d data."
    ):
        parametric_bootstrap(RANDOM_10x5, 1, family="norm")


def test_invalid_family():
    with pytest.raises(ValueError):
        parametric_bootstrap(RANDOM_10x1, 1, family="snorf")
