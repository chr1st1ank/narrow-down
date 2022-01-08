"""Nox sessions."""
import platform
import sys

import nox
from nox.sessions import Session

nox.options.sessions = ["tests", "mypy"]
python_versions = ["3.7", "3.8", "3.9", "3.10"]


def install_with_constraints(session: Session, *args: str) -> None:  # noqa
    """Install packages constrained by Poetry's lock file.

    This function is a wrapper for nox.sessions.Session.install. It
    invokes pip to install packages inside of the session's virtualenv.
    Additionally, pip is passed a constraints file generated from
    Poetry's lock file, to ensure that the packages are pinned to the
    versions specified in poetry.lock. This allows you to manage the
    packages as Poetry development dependencies.

    Arguments:
        session: The Session object.
        args: Command-line arguments for pip.
    """
    session.install("maturin")
    maturin_cmd = ["maturin", "develop", "--release"]
    if "darwin" in sys.platform.lower():
        maturin_cmd.append("--universal2")
    session.run(*maturin_cmd)
    session.install(".", *args)


@nox.session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    install_with_constraints(
        session, "invoke", "pytest", "xdoctest", "coverage[toml]", "pytest-asyncio", "pytest-cov"
    )
    try:
        session.run(
            "inv",
            "tests",
            env={
                "COVERAGE_FILE": f".coverage.{platform.system()}.{platform.python_version()}",
            },
        )
    finally:
        if session.interactive:
            session.notify("coverage")


@nox.session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs if session.posargs and len(session._runner.manifest) == 1 else []  # noqa
    install_with_constraints(session, "invoke", "coverage[toml]")
    session.run("inv", "coverage", *args)


@nox.session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    install_with_constraints(session, "invoke", "mypy")
    session.run("inv", "mypy")


@nox.session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    install_with_constraints(session, "invoke", "safety")
    session.run("inv", "safety")
