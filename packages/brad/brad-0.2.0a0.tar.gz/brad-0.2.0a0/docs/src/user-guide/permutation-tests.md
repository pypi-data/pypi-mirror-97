## Background

Permutation tests are a means for comparing samples from two populations, and
understanding whether the populations they are drawn from are different. They
were first introduced by [Fisher](https://en.wikipedia.org/wiki/Ronald_Fisher)
and have subsequently become a popular method.

Suppose we have samples drawn from two distributions

$$
    \begin{aligned}
        X_1, \dots, X_n \sim F \\
        Y_1, \dots, Y_m \sim G
    \end{aligned}
$$

and we want to understand whether $F$ and $G$ are different. As a concrete
example, suppose $X_i$ represent the test scores of students who participated in
an after-school coaching program, and $Y_i$ represent the test scores of
students who did not participate. Perhaps the data looks something like this

```
Coached: 70, 74, 81, 95, 88
Not coached: 60, 80, 75, 70, 76, 78, 82, 88
```

The students who receive coaching have an average score of $81.6$, whereas the
students who did not receive coaching have an average score of $76.125$, so it
seems that the coached students did slightly better, but as ever, we want to
know how significant this difference is.

## Permutation test

Let the
[null hypothesis](https://en.wikipedia.org/wiki/Exclusion_of_the_null_hypothesis)
be that the two distributions are the same: $H_0: F = G$. Under the null
hypothesis, any one of the observed test scores is equally likely to have come
from the coached students, or the students who were not coached. If the null
hypothesis were true, we would still expect to see some difference in the two
means due to sampling variance. The question is just how much?

To estimate how much the means might vary even if the distributions were the
same, we can take the observations and randomly allocate them to the two groups.
We then compute the difference in means on each of the random allocations giving
us a distribution of the test statistic. By comparing the observed value to the
replications we can determine whether the observed difference in means is
actually surprising, or if it is in fact consistent with the assumption that
there is no difference between the two distributions.

## Permutation tests in `brad`

We can analyse the above data in `brad`. First let's create the data and labels
as NumPy arrays.

```python
import numpy as np

data = np.array([70, 74, 81, 95, 88, 60, 80, 75, 70, 76, 78, 82, 88])
labels = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
```

We define a function to apply to data and labels, in this case the difference in
means

```python
def mean_diff(data, labels):
    return data[labels == 1].mean() - data[labels == 0].mean()
```

Then we can used `brad.permutation_test` to generate the permutation
distribution, with the chosen statistic applied to each sample.

```python
from brad import permutation_test

permutation_dist = permutation_test(
    data, labels, n_samples=10_000, statistic=mean_diff
)
```

We can then measure how extreme the original observation was by counting how
many of the replications are greater than it using the
`PermutationDistribution.p_value` method

```python
permutation_dist.p_value()
```

In this case, we see that about 14% of the samples where the labels had no
relation to the data had a larger mean difference, so we perhaps should not
consider our observed mean difference as so significant.
