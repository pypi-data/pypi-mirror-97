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
class Resample:
    """
    Dataclass used when returning resampled data.

    Attributes:
        data: Either the original data, _or_ the original data mapped with the
            supplied statistic.
        samples: Samples produced by the chosen method, mapped with the
            supplied statistic.
    """

    data: Numeric
    samples: np.ndarray

    def _1d_check(self, method: str):
        if np.array(self.data).ndim != 0 or self.samples.ndim != 1:
            raise ValueError(
                f"{method} can only be calculated for a scalar statistic."
            )

    def standard_error(self, ddof: int = 1):
        """
        Compute the standard error of the samples.

        Args:
            ddof: "Delta degrees of freedom". The divisor used when calculating
                the standard deviation of the samples is `num_samples - ddof`.
                Defaults to `1` as per the original definition of the bootstrap
                standard error.
        """
        self._1d_check("Standard error")
        return self.samples.std(ddof=ddof)

    def confidence_interval(
        self, confidence_level=0.95, kind: str = "pivotal"
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
                self.samples,
                [(1 - confidence_level) / 2, (1 + confidence_level) / 2],
            )
            return ConfidenceInterval(
                lower=2 * self.data - upper_quantile,
                upper=2 * self.data - lower_quantile,
                kind="pivotal",
                confidence_level=confidence_level,
            )
        elif kind.lower() == "normal":
            z = norm.ppf((1 + confidence_level) / 2)
            se = self.standard_error()
            return ConfidenceInterval(
                lower=self.data - z * se,
                upper=self.data + z * se,
                kind="normal",
                confidence_level=confidence_level,
            )
        elif kind.lower() == "percentile":
            quantiles = [
                (1 - confidence_level) / 2,
                (1 + confidence_level) / 2,
            ]
            lower, upper = np.quantile(self.samples, quantiles)
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
