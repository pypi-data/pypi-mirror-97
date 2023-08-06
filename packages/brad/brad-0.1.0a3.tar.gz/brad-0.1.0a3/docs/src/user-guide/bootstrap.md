## Non-parametric bootstrap

Suppose that we have a sample from a probability distribution $X_1, \dots, X_n$
from which we compute a statistic of interest $T_n := f(X_1, \dots, X_n)$. We
use the notation $T_n$ to emphasise that the sampling distribution of the
statistic will typically depend on the size of the sample it is computed on.

We would like to compute $\mathrm{var}(T_n)$. To do so we sample with
replacement from $X_1, \dots, X_n$ to generate a large number $B$ of _bootstrap
samples_

$$
    X^*_{1,b}, \dots, X^*_{n,b} \quad\quad b=1,\dots,B
$$

We compute the statistic of interest on each bootstrap sample to generate
_bootstrap replications_ of the statistic

$$
    T^*_{n, b} = g(X^*_{1,b}, \dots, X^*_{n,b}) \quad\quad b=1,\dots,B
$$

The distribution of $T^*_n$ is known as the _bootstrap distribution_. It is
_not_ the same as the sampling distribution of $T_n$. However, we can use it to
estimate standard errors and confidence intervals.

Sampling with replacement from the original data is often referred to simply as
the bootstrap, but also sometimes referred to as the non-parametric bootstrap,
to distinguish it from [the parametric bootstrap](#the-parametric-bootstrap) and
[the smooth bootstrap](#the-smooth-bootstrap).

For the non-parametric bootstrap simply import `bootstrap` from `brad`. You can
specify how many bootstrap samples should be drawn with the `n_samples`
argument, and a statistic to be applied to each sample with the `statistic`
keyword argument. In this example, our data is a random sample from a normal
distribution, and we calculate 10,000 bootstrap replications of the standard
deviation.

```python
import numpy as np
from brad import bootstrap

data = np.random.normal(0, 1, size=50)

resample = bootstrap(data, n_samples=10_000, statistic=np.std)
```

The returned object is a `brad.models.Resample` dataclass, which contains the
original statistic under the `.data` attribute, and the replications under the
`.sample` attribute. It is also capable of calculating various quantities of
interest for you.

## Standard error

The bootstrap standard error is calculated as the standard deviation of the
bootstrap replications. That is

$$
    \hat{se}_{boot} := \left(\frac{1}{B - 1} \sum_{b=1}^B \left( T^*_{n,b} - \frac 1 B \sum_{r=1}^B T^*_{n,r} \right)^2\right)^{1 / 2}
$$

In `brad`, simply call the `standard_error` method on the `Resample` dataclass

```python
resample.standard_error()
```

## Confidence intervals

There are three common methods for calculating confidence intervals from the
bootstrap distribution.

### Normal interval

To calculate a normal confidence interval with confidence level $1 - \alpha$ we
first define $z_{\alpha/2} := \Phi^{-1}(1 - (\alpha / 2))$ where $\Phi^{-1}$ is
the inverse CDF of the standard normal distribution. We then define the _normal
interval_ to be

$$
    T_n \pm z_{\alpha / 2} \hat{se}_{boot}
$$

This could be a poor approximation if the sampling distribution of $T_n$ is not
close to a normal distribution. Normal intervals can be calculated in `brad`
using the argument `#!python kind="normal"` in the `confidence_interval` method
of the `Resample` class

```python
resample.confidence_interval(kind="normal")
```

### Percentile interval

Let $T^*_{n, \beta}$ denote the $\beta$-th quantile of the bootstrap
distribution of $T_n$. The percentile confidence interval is given by

$$
    \left( T^*_{n, \alpha/2}, T^*_{n, 1-\alpha/2} \right)
$$

Percentile intervals can be calculated in `brad` using the argument
`#!python kind="percentile"` in the `confidence_interval` method of the
`Resample` class

```python
resample.confidence_interval(kind="percentile")
```

### Pivotal interval

Let $T$ denote the true value of the quantity being estimated by $T_n$, and
define _the pivot_ $R_n := T_n - T$, which is simply the difference between our
estimate and the true value. Of course, $T$ is not known to us, that's why we're
trying to estimate it in the first place, but let's deal with that problem
later.

Let $H(r) = \mathbb P(R_n <= r)$ be the CDF of the pivot, and $H^{-1}$ be its
inverse and define

$$
    a := T_n - H^{-1}\left(1 - \frac \alpha 2\right) \quad b:= T_n - H^{-1}\left(\frac \alpha 2 \right)
$$

It follows that

$$
\begin{aligned}
    \mathbb P(a \leq T \leq b) &= \mathbb P(T_n - b \leq T_n -T \leq T_n - a) \\
    &= H(T_n - a) - H(T_n - b) \\
    &= H\left(H^{-1}\left(1 - \frac \alpha 2\right) \right) - H\left(H^{-1}\left(\frac \alpha 2\right) \right) \\
    &= 1 - \alpha
\end{aligned}
$$

so $(a, b)$ meets the requirements of a $1 - \alpha$ confidence interval.
However, we can't compute it directly. Instead we estimate it using the
bootstrap samples.

Let $R^*_{n,b} := T^*_{n,b} - T_n$. This is our bootstrap estimate of the pivot.
Note also that we can estimate the inverse CDF of the pivot using sample
quantiles of the estimated pivot. Specifically let $r^*_\beta$ denote the
$\beta$ sample quantile of $T^*_{n,b}$ and note that
$r^*_\beta = T^*_{n,\beta} - T_n$, so we have

$$
\begin{aligned}
    \hat a &= T_n - r^*_{1 - \alpha / 2} = 2T_n - T^*_{n,1-\alpha/2} \\
    \hat b &= T_n - r^*_{\alpha / 2} = 2T_n - T^*_{n,\alpha/2}
\end{aligned}
$$

The pivotal confidence interval is given by

$$
    \left( 2T_n - T^*_{n, 1-\alpha/2}, 2T_n - T^*_{n, \alpha/2} \right)
$$

Pivotal intervals can be calculated in `brad` using the argument
`#!python kind="pivotal"` (which is also the default option) in the
`confidence_interval` method of the `Resample` class

```python
resample.confidence_interval(kind="pivotal")
```

## The parametric bootstrap

The parametric bootstrap is very similar to the non-parametric bootstrap, but
rather than sampling with replacement from the original sample, we sample from a
parametric distribution whose parameters are estimated from the data. Some of
the pros and cons of this approach include:

- In the non-parametric bootstrap, if bootstrap samples are taken from a small
  original sample, then the bootstrap samples might replicate artifacts of the
  discreteness, that is not representative of the distribution that produced the
  sample in the first place.
- Furthermore, finite samples have a restricted range, and hence non-parametric
  bootstrap samples are prone to underestimating the variance of the true
  distribution.
- The parametric bootstrap does not have this problem off replicating artifacts
  of the discreteness of a finite sample, and might be better able to sample
  from the tails of a distribution, but it comes with the cost of making a
  parametric assumption about the data.
- Estimating the parameters of the parametric distribution is often done using
  methods that are based on asymptotic behaviour in the limit of a large sample,
  and hence might not always be appropriate for effectively modelling small
  samples.

The parametric bootstrap can be performed with `brad` using a very similar
interface to the non-parametric bootstrap. You must specify the parametric
family from which the sample is assumed to be drawn, and `brad` will fit a
distribution from that family to the data, and draw samples from it. Under the
hood, `brad` simply uses the relevant distribution from `scipy.stats`.

Here's an example

```python
import numpy as np
from brad import parametric_bootstrap

rng = np.random.default_rng()
data = rng.normal(3, 2, size=20)

resample = parametric_bootstrap(
    data, n_samples=10_000, statistic=np.mean, family="norm"
)
```

As with the non-parametric bootstrap, you can compute standard errors and
confidence intervals from the `Resample` object.

## The smooth bootstrap

An alternative to addressing some of the problems of the non-parametric
bootstrap, specifically artifacts of discreteness and underestimates of
variation, is to first smooth the empirical data distribution with a
[kernel density estimator](https://en.wikipedia.org/wiki/Kernel_density_estimation)
and then draw bootstrap samples from the smoothed distribution. This is known as
the smooth bootstrap.

This approach might not work so well for heavily skewed distributions as the
smoothing often has a symmetrising effect. Furthermore, we have the problem of
choosing an appropriate smoothing kernel, which is not always obvious. Finally
smoothing a distribution like this has the problem of potentially introducing
impossible values. For example, smoothing positive values might place positive
probability on some negative values.

As with the parametric and non-parametric bootstrap, the smooth bootstrap can be
performed in `brad` using a very similar interface. You must specify a kernel
and a bandwidth, and `brad` will smooth the samples using a kernel density
estimator from scikit-learn.

Here's an example

```python
import numpy as np
from brad import smooth_bootstrap

rng = np.random.default_rng()
# scikit-learn expects a 2D array
data = rng.normal(3, 2, size=(20, 1))

resample = smooth_bootstrap(
    data, n_samples=10_000, statistic=np.mean, kernel="gaussian", bandwidth=0.2
)
```
