from brad.resample import (
    bootknife,
    bootstrap,
    jackknife,
    parametric_bootstrap,
    permutation_test,
    smooth_bootstrap,
)

try:
    from importlib.metadata import (  # type: ignore
        PackageNotFoundError,
        version,
    )
except ModuleNotFoundError:
    # if using Python 3.7, import from the backport
    from importlib_metadata import (  # type: ignore
        PackageNotFoundError,
        version,
    )

try:
    __version__ = version("brad")
except PackageNotFoundError:
    # package is not installed
    pass


__all__ = [
    "bootknife",
    "bootstrap",
    "jackknife",
    "parametric_bootstrap",
    "permutation_test",
    "smooth_bootstrap",
]
