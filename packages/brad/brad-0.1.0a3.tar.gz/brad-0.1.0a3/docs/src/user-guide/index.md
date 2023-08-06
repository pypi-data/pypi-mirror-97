The bootstrap is a statistical technique for numerically estimating the sampling
distribution of almost any statistic using simple resampling methods. It was
introduced to the world by
[Bradley Efron](https://en.wikipedia.org/wiki/Bradley_Efron) (after whom `brad`
is named) in 1979.

In this first section of the user guide we'll recap the basic ideas and theory
behind the bootstrap. In subsequent sections we'll show how those methods and
techniques are implemented in `brad`.

## Motivation

Suppose we are given a coin and we flip it 20 times. We record 13 heads and 7
tails. Having observed almost twice as many heads as tails, we might wonder if
the coin is more likely to land heads rather than tails, so we decide to
investigate.

We model each flip of the coin as a Bernoulli random variable with fixed
probability $p$ of the coin landing heads, that is

$$
    X_i \sim \mathrm{Bernoulli}(p) \quad\quad i = 1, \dots, 20
$$

where we interpret $X_i = 1$ as meaning that the ith coin landed heads, and
$X_i = 0$ as the ith coin landed tails.

Using either the
[method of moments](<https://en.wikipedia.org/wiki/Method_of_moments_(statistics)>)
or a
[maximum likelihood estimate](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
we arrive at the same estimate of $p$ which is simply the sample mean, i.e.

$$
    \hat{p}_{20} = \frac{1}{20} \sum_{i=1}^n X_i = 0.65
$$

<!--prettier-ignore-start-->
!!! note
    We use the notation $\hat p_{20}$ to emphasise that the sampling
    distribution of the statistic _depends on the sample size_. Indeed if we
    were to calculate the sample mean from 10, or 100 samples, these would
    yield different statistics with different sampling distributions.
<!--prettier-ignore-end-->

So our best estimate based on the collected data is that the coin has
probability $0.65$ of landing heads. But how accurate is this estimate? If we
were to repeat the experiment we probably wouldn't get exactly 13 heads again.
We would get a different result, which in turn would mean a different estimate
$\hat p_{20}$.

A natural question therefore is if $\hat{p}_{20}$ could have been different had
we collected different data, then by how much?

## The sampling distribution

The sampling distribution of a statistic captures how the statistic could vary
if the data the statistic was computed from were resampled.

In this simple example we can easily compute sampling distributions if $p$ is
known. For example, the below figure shows a histogram of the value of
$\hat p_{20}$ over $10,000$ repeats of the experiment with a fair coin, i.e.
$p = 0.5$.

![Sampling distribution](../static/images/sampling-distribution.png)

In this case, we can see that there is enough variability in the sampling
distribution that 13 heads and 7 tails is not so unlikely. In fact the
probability of getting 13 or more heads in 20 flips of a fair coin is about 13%,
not that much more unlikely than rolling a 6 on a fair die. So we probably
shouldn't be too surprised to see the result we have.

<!--prettier-ignore-start-->
!!! note
    The experiment we just did of seeing how likely the observed data would be
    under the assumption that the coin is fair is formalised in the concept of
    a
    [hypothesis test](https://en.wikipedia.org/wiki/Statistical_hypothesis_testing),
    and the 13% figure we came up with in the concept of a
    [p-value](https://en.wikipedia.org/wiki/P-value).
<!--prettier-ignore-end-->

## Standard error

Now that we know our estimate could be wrong simply because of sampling
variability, we want to quantify _how wrong_ it could be. In the case of the
sample mean, we actually have a pretty precise formula courtesy of the
[Central Limit Theorem](https://en.wikipedia.org/wiki/Central_limit_theorem),
that is the estimated standard error is given by

$$
    \hat{\mathrm{se}} := \sqrt{\frac{\frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2}{n}}
$$

where $\bar X$ is the sample mean

$$
    \bar X := \frac 1 n \sum_{i=1}^n X_i
$$

We should expect the sample mean to be within 1 standard error of the true mean
approximately 68% of the time, and within 2 standard errors of the true mean
approximately 95% of the time. In the the coin flipping example above we have
$\mathrm{se} \approx 0.11$, so the sample mean $\hat p_{20}$ is only $1.37$
standard errors from $0.5$, and hence we again see that our result is not so
significant.

<!--prettier-ignore-start-->
!!! note
    This calculation we just did is roughly equivalent to calculating a
    [confidence interval](https://en.wikipedia.org/wiki/Confidence_interval)
    for our estimate of the sample mean.
<!--prettier-ignore-end-->

We can compare the estimated standard error to the true standard error (the
standard deviation of the sampling distribution) by resampling the data,
calculating the mean on each sample, and then computing the standard deviation
of those samples

```python
import numpy as np

rng = np.random.default_rng()
standard_error = (rng.binomial(20, 0.5, size=100_000) / 20).std()
```

We find the true standard deviation is about $0.112$, very close to our
estimate.

However, in many cases we don't have access to a nice formula for the standard
error, and we also aren't able to simply draw more samples from the distribution
we are studying, so what should we do in that scenario?

## The plugin principle

We know that if we could collect new data and repeat our analysis many times we
could estimate the sampling distribution and hence standard error of our
statistic. The plugin principle says that rather than collect new data, we can
sample from an approximation to the true data distribution. That is to say we
exactly perform this analysis where we draw new samples, compute the statistic
of interest on those samples and analyse the sampling distribution, but we "plug
in" an approximation to the data distribution.

The simplest approximation to the data distribution is the empirical
distribution, that is to say, to simulate a draw from the data distribution, we
just pick one of our observations at random. To draw a sample, we just sample
with replacement from the observations. Let's see how this looks with the simple
example above.

```python
import numpy as np

rng = np.random.default_rng()

# 20 flips, 13 heads, 7 tails
data = np.zeros(20)
data[:13] = 1

# sample 20 observations with replacement 10,000 times and calculate the mean
samples = rng.choice(data, size=(10_000, data.shape[0]))
bootstrap_dist = samples.mean(axis=1)

# estimated standard error is the mean of the bootstrap distribution
standard_error = bootstrap_dist.std()
```

With this approach we estimate the standard error to be approximately $0.106$,
very close to the answers we got by other methods.

## Meet `brad`

Let's look at what the above example looks like with brad.

```python
import numpy as np
from brad import bootstrap

data = np.zeros(20)
data[:13] = 1

resample = bootstrap(data, n_samples=10_000, statistic=np.mean)
resample.standard_error()
```

which gets us the same answer as before. But `brad` can do more for us than just
that. For example we can also easily calculate confidence intervals

```python
resample.confidence_inferval(confidence_level=0.95)
```

We'll take a more detailed tour of `brad` over the course of the rest of this
user guide.
