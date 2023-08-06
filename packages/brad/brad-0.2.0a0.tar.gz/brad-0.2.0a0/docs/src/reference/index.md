`brad` exposes high-level interfaces for computing the bootstrap and its
variants, and permutation tests. These are documented below.

The high-level interfaces are built with two building blocks: samplers and
result dataclasses. Samplers yield samples according to the chosen strategy,
while the result dataclasses encapsulate the results of sampling and can perform
basic calculations.

## Bootstrap and variants

<!-- prettier-ignore-start -->
::: brad.resample
    handler: python
    selection:
      members:
        - bootstrap
        - parametric_bootstrap
        - smooth_bootstrap
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->

## Bootknife

<!-- prettier-ignore-start -->
::: brad.resample
    handler: python
    selection:
      members:
        - bootknife
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->

## Jacknife

<!-- prettier-ignore-start -->
::: brad.resample
    handler: python
    selection:
      members:
        - jackknife
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->

## Permutation tests

<!-- prettier-ignore-start -->
::: brad.resample
    handler: python
    selection:
      members:
        - permutation_test
    rendering:
      heading_level: 3
      show_root_toc_entry: false
<!-- prettier-ignore-end -->
