from dataclasses import dataclass
from typing import Union

import numpy as np
from scipy.stats import norm

Numeric = Union[float, np.ndarray]


@dataclass(frozen=True)
class ConfidenceInterval:
    """
    Confidence interval computed from bootstrap samples.

    Attributes:
        lower: The lower endpoint of the interval.
        upper: The upper endpoint of the interval.
        kind: The method used to construct the interval. Will be one of
            `"pivotal"`, `"normal"`, and `"percentile"`.
        confidence_level: The confidence level of the interval.
    """

    lower: float
    upper: float
    kind: str
    confidence_level: float


@dataclass(frozen=True)
class Distribution:
    observation: Numeric
    replications: np.ndarray

    def _1d_check(self, method: str) -> None:
        if np.array(self.observation).ndim != 0 or self.replications.ndim != 1:
            raise ValueError(
                f"{method} can only be calculated for a scalar statistic."
            )


@dataclass(frozen=True)
class BootstrapDistribution(Distribution):
    """
    Dataclass used when returning bootstrapped statistics.

    Attributes:
        observation: The statistic applied to the original data.
        replications: Bootstrap replications of the statistic. Each entry
            corresponds to the statistic applied to a bootstrap sample.
    """

    def standard_error(self, ddof: int = 1) -> float:
        """
        Compute the standard error of the samples.

        Args:
            ddof: "Delta degrees of freedom". The divisor used when calculating
                the standard deviation of the samples is `num_samples - ddof`.
                Defaults to `1` as per the original definition of the bootstrap
                standard error.
        """
        self._1d_check("Standard error")
        return self.replications.std(ddof=ddof)

    def confidence_interval(
        self, confidence_level: float = 0.95, kind: str = "pivotal"
    ) -> ConfidenceInterval:
        """
        Compute a confidence interval from the samples. Can compute pivotal,
        percentile, or normal intervals.

        Args:
            confidence_level: The confidence level of the interval, stated as a
                number between `0` and `1`. If the confidence level is `0.95`
                (the default value) then the resulting confidence interval
                would contain the true value of the quantity being estimated
                95% of the time when calculated on different samples.
            kind: The type of interval to construct. Options are `"pivotal"`,
                `"percentile"` and `"normal"`.

        Returns:
            The upper and lower bounds for the interval.
        """
        self._1d_check("Confidence intervals")
        if kind.lower() == "pivotal":
            lower_quantile, upper_quantile = np.quantile(
                self.replications,
                [(1 - confidence_level) / 2, (1 + confidence_level) / 2],
            )
            return ConfidenceInterval(
                lower=2 * self.observation - upper_quantile,
                upper=2 * self.observation - lower_quantile,
                kind="pivotal",
                confidence_level=confidence_level,
            )
        elif kind.lower() == "normal":
            z = norm.ppf((1 + confidence_level) / 2)
            se = self.standard_error()
            return ConfidenceInterval(
                lower=self.observation - z * se,
                upper=self.observation + z * se,
                kind="normal",
                confidence_level=confidence_level,
            )
        elif kind.lower() == "percentile":
            quantiles = [
                (1 - confidence_level) / 2,
                (1 + confidence_level) / 2,
            ]
            lower, upper = np.quantile(self.replications, quantiles)
            return ConfidenceInterval(
                lower=lower,
                upper=upper,
                kind="percentile",
                confidence_level=confidence_level,
            )
        else:
            raise ValueError(
                f"Invalid option '{kind}' for argument kind. Should be one "
                "of: 'pivotal', 'normal', 'percentile'."
            )


@dataclass(frozen=True)
class PermutationDistribution(Distribution):
    """
    Dataclass used when returning bootstrapped statistics.

    Attributes:
        observation: The statistic applied to the original data.
        replications: Replications of the statistic on the data with labels
            permuted. Each entry corresponds to a single permutation.
    """

    def p_value(self, lower_tail: bool = False) -> float:
        self._1d_check("P values")

        if lower_tail:
            return (self.replications < self.observation).mean()
        else:
            return (self.replications > self.observation).mean()
