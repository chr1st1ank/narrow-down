"""Nox sessions."""
import platform

import nox
from nox.sessions import Session

nox.options.sessions = ["tests", "benchmarks"]
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
    maturin_cmd = ["maturin", "develop", "--release", "--extras=scylladb"]
    session.run(*maturin_cmd)
    session.install(".", *args)


@nox.session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    install_with_constraints(
        session,
        "pytest",
        "xdoctest",
        "coverage[toml]",
        "pytest-asyncio",
        "pytest-benchmark",
        "pytest-cov",
    )
    try:
        session.run(
            "task",
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
    install_with_constraints(session, "coverage[toml]")
    session.run("task", "coverage", *args)


@nox.session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    install_with_constraints(session, "safety")
    session.run("task", "safety")


@nox.session(python=python_versions)
def benchmarks(session: Session) -> None:
    """Produce the coverage report."""
    install_with_constraints(
        session,
        "pytest",
        "xdoctest",
        "coverage[toml]",
        "pytest-asyncio",
        "pytest-benchmark",
        "pytest-cov",
    )
    session.run("task", "benchmarks")
