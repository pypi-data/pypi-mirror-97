## Overview

`brad` uses custom dataclasses to return results from its various high-level
interfaces. This is so that results are both explicit and discoverable, but also
so that common computations can be exposed as methods of those classes.

For example, the bootstrap and its variants return a `BootstrapDistribution`
class, which is able to calculate standard error and confidence intervals

```python
import numpy as np
from brad.results import BootstrapDistribution

bootstrap_dist = BootstrapDistribution(
    observation=0, replications=np.arange(-2, 3)
)

# compute standard error of the replications
bootstrap_dist.standard_error()

# compute a confidence interval
bootstrap_dist.confidence_interval()
```

The `confidence_interval` method itself returns a dataclass of type
`ConfidenceInterval`. This contains the endpoints of the interval under `upper`
and `lower` but also includes metadata such as the `confidence_level` and the
method used to compute the interval.

## Reference

<!-- prettier-ignore-start -->
::: brad.results
    handler: python
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->
