import shutil
import warnings

import nox


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return f"UserWarning: {msg}\n"


warnings.formatwarning = custom_formatwarning  # type: ignore

# don't run format session by default
nox.options.sessions = ["lint", "test"]

SOURCES = ["src", "tests", "noxfile.py"]


@nox.session()
def lint(session):
    """Lint all source code"""
    session.install("black", "flake8", "isort", "mypy")
    session.run("black", "--check", *SOURCES)
    session.run("flake8", *SOURCES)
    session.run("isort", "--check", *SOURCES)
    session.run("mypy", *SOURCES)


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    """Run tests"""
    session.install(".")
    session.install("pytest", "pytest-cov")
    session.run("pytest")


@nox.session(name="format")
def format_(session):
    """Format all source code"""
    session.install("black", "isort")
    session.run("black", *SOURCES)
    session.run("isort", *SOURCES)

    if shutil.which("prettier") is None:
        warnings.warn(
            "Prettier is not installed. Docs have not been formatted.\n\n"
            "Visit https://prettier.io/ to install.",
            stacklevel=0,
        )
    else:
        session.run("prettier", "--write", "docs", "README.md", external=True)


@nox.session()
def build(session):
    """Build package"""
    session.install(".", "build")
    session.run(
        "python", "-m", "build", "--sdist", "--wheel", "--outdir", "dist/"
    )


@nox.session(name="build-docs")
def build_docs(session):
    """Build documentation"""
    session.install(".")
    session.chdir("docs")
    session.install("-r", "requirements-docs.txt")
    session.run("mkdocs", "build")
