## Overview

In `brad` sampling is handled by `Sampler` classes. For example, for the
non-parametric bootstrap, `brad` uses `brad.samples.NonParametricSampler` under
the hood.

```python
import numpy as np
from brad.samplers import NonParametricSampler

data = np.arange(10)

sampler = NonParametricSampler(data)

for i, sample in enumerate(sampler):
    if i >= 10:
        break
    print(sample)
```

The sampler will yield samples forever, it is the responsibility of the code
using the sampler to control the sample size. More often, you will want to use
the higher level interfaces in `brad`.

## Reference

`brad` includes the following samplers. Any custom samplers should inherit from
the `Sampler` class.

<!-- prettier-ignore-start -->
::: brad.samplers
    handler: python
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->
