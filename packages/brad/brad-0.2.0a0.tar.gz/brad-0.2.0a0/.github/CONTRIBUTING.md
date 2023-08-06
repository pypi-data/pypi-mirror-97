# Contributing to brad

Contributions are welcome. This guide should tell you everything you need to
know.

## Cloning

To develop on `brad` you'll need a fork of this repo that you can work from.
The easiest option is to install the [GitHub CLI](https://cli.github.com/) and
run the command

```sh
gh repo fork tcbegley/brad
```

Alternatively create a fork in the web UI and clone it.

## Development

You can install `brad` and its dependencies from source from the root of this
repo with

```sh
python -m pip install .
```

Tests and linters are run with [`nox`][nox]. Install with

```sh
python -m pip install nox
```

You can then run one of the pre-configured nox "sessions" with

```sh
nox -s lint
```

The available sessions are:
- `lint`: run source code linters (`black`, `flake8`, `isort`, `mypy`)
- `test`: run test suite with PyTest. Will try to run on Python 3.7, 3.8 and
3.9.
- `test-3.x`: run tests for only Python 3.x (replace x with 7, 8, or 9)
- `format`: format source code with `black` and `isort`.
- `build`: build sdist and wheel.

Running only the command

```sh
nox
```

will run `lint` and `test` by default (so in particular `nox` will not format
the source code unless explicitly told to do so).

## Releasing

Releases are published to PyPI automatically when a new GitHub release is
published. Only maintainers of `tcbegley/brad` will have the permissions to do
this. Releases can either be made via the web UI or using the GitHub CLI

```sh
gh release create vX.X.X [--prerelease]
```

Brad uses [setuptools-scm](https://github.com/pypa/setuptools_scm) to
automatically set the version number based on git tags, so there is no need to
hardcode the version anywhere.

Brad uses [semantic versioning](https://semver.org/spec/v2.0.0.html). Please
adhere to that pattern when choosing a version number.

[nox]: https://nox.thea.codes
