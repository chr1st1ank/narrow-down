"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
# pylint: disable=unused-argument,import-error
import platform
import sys
import webbrowser
from pathlib import Path

from invoke import call, task
from invoke.context import Context
from invoke.runners import Result

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
SOURCE_DIR = ROOT_DIR.joinpath("narrow_down")
TEST_DIR = ROOT_DIR.joinpath("tests")
PYTHON_TARGETS = [
    SOURCE_DIR,
    TEST_DIR,
    ROOT_DIR.joinpath("noxfile.py"),
    Path(__file__),
]
PYTHON_TARGETS_STR = " ".join([str(p) for p in PYTHON_TARGETS])


def _shorten(long_text: str) -> str:
    if len(long_text) <= 100:
        return long_text
    return long_text[:97] + "..."


def _escape_unicode_on_windows(unicode_text: str):
    if sys.platform == "win32":
        return unicode_text.encode(encoding="ascii", errors="?")
    return unicode_text


def _run(c: Context, command: str) -> Result:
    print(_escape_unicode_on_windows("⏳"), "Running", _shorten(command))
    return c.run(command, pty=platform.system() != "Windows")


@task()
def develop(c):
    # type: (Context) -> None
    """Rebuild the Rust library and install all missing dependencies."""
    _run(c, "maturin develop --release --extras dev,docs,experiments")


@task()
def protobuild(c):
    # type: (Context) -> None
    """Build the protobuf objects."""
    _run(
        c,
        "protoc -I . --python_out=narrow_down/ --mypy_out=narrow_down/ proto/stored_document.proto",
    )


@task()
def clean_rust(c):
    # type: (Context) -> None
    """Clean up files from Rust built."""
    _run(c, "cargo clean")
    _run(c, "cargo clean --release")


@task()
def clean_build(c):
    # type: (Context) -> None
    """Clean up files from package building."""
    _run(c, "rm -fr build/")
    _run(c, "rm -fr dist/")
    _run(c, "rm -fr .eggs/")
    _run(c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(c, "find . -name '*.egg' -exec rm -f {} +")


@task()
def clean_python(c):
    # type: (Context) -> None
    """Clean up python file artifacts."""
    _run(c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(c, "find . -name '*~' -exec rm -f {} +")
    _run(c, "find . -name '__pycache__' -exec rm -fr {} +")


@task()
def clean_tests(c):
    # type: (Context) -> None
    """Clean up files from testing."""
    _run(c, f"rm -f {COVERAGE_FILE}")
    _run(c, f"rm -fr {COVERAGE_DIR}")
    _run(c, "rm -fr .pytest_cache")


@task()
def clean_docs(c):
    # type: (Context) -> None
    """Clean up files from documentation builds."""
    _run(c, f"rm -fr {DOCS_BUILD_DIR} {DOCS_DIR}/apidoc")
    # _run(c, f"rm -f {DOCS_DIR}/modules.rst {DOCS_DIR}/narrow_down.rst")


@task(
    help={
        "serve": "Build the docs watching for changes",
        "open_browser": "Open the docs in the web browser",
    }
)
def docs(c, serve=False, open_browser=False):
    # type: (Context, bool, bool) -> None
    """Build documentation."""
    _run(
        c,
        "jupyter-nbconvert -TagRemovePreprocessor.remove_cell_tags remove_cell "
        "--to markdown docs/user_guide/*.ipynb",
    )
    _run(
        c,
        f"sphinx-apidoc --module-first -d 1 --no-toc --separate -o {DOCS_DIR}/apidoc {SOURCE_DIR}",
    )
    build_docs = f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}"
    _run(c, build_docs)
    if open_browser:
        webbrowser.open(DOCS_INDEX.absolute().as_uri())
    if serve:
        _run(c, f"watchmedo shell-command -p '*.rst;*.md' -c '{build_docs}' -R -D .")


@task(pre=[clean_rust, clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    # type: (Context) -> None
    """Run all clean sub-tasks."""


@task()
def install_hooks(c):
    # type: (Context) -> None
    """Install pre-commit hooks."""
    _run(c, "pre-commit install")


@task()
def hooks(c):
    # type: (Context) -> None
    """Run pre-commit hooks."""
    _run(c, "pre-commit run --all-files")


@task(name="format", help={"check": "Checks if source is formatted without applying changes"})
def format_(c, check_=False):
    # type: (Context, bool) -> None
    """Format code."""
    isort_options = ["--check-only", "--diff"] if check_ else []
    _run(c, f"isort {' '.join(isort_options)} {PYTHON_TARGETS_STR}")
    black_options = ["--diff", "--check"] if check_ else ["--quiet"]
    _run(c, f"black {' '.join(black_options)} {PYTHON_TARGETS_STR}")


@task()
def flake8(c):
    # type: (Context) -> None
    """Run flake8."""
    _run(c, f"flakeheaven lint {PYTHON_TARGETS_STR}")


@task()
def safety(c):
    # type: (Context) -> None
    """Run safety."""
    _run(
        c,
        "poetry export --dev --format=requirements.txt --without-hashes | "
        "safety check --stdin --full-report",
    )


@task(pre=[flake8, safety, call(format_, check=True)])
def lint(c):
    # type: (Context) -> None
    """Run all linting."""


@task()
def mypy(c):
    # type: (Context) -> None
    """Run mypy."""
    _run(c, f"mypy --follow-imports silent --python-version 3.8 {PYTHON_TARGETS_STR}")


@task()
def pylint(c):
    # type: (Context) -> None
    """Run pylint."""
    _run(c, f"pylint {PYTHON_TARGETS_STR}")


@task()
def doctest(c):
    # type: (Context) -> None
    """Run tests."""
    pytest_options = [
        "--xdoctest",
        "--nbmake",
        "docs/user_guide",
        "--benchmark-disable",
    ]
    _run(c, f"pytest {' '.join(pytest_options)}")


@task()
def tests(c):
    # type: (Context) -> None
    """Run tests."""
    pytest_options = [
        "--xdoctest",
        "--cov",
        "--cov-report=",
        "--cov-fail-under=0",
        "--benchmark-disable",
    ]
    _run(c, f"pytest {' '.join(pytest_options)} {TEST_DIR} {SOURCE_DIR}")


@task()
def benchmarks(c):
    # type: (Context) -> None
    """Run benchmark tests."""
    pytest_options = [
        "--benchmark-only",
        "--benchmark-sort=name",
    ]
    _run(c, f"pytest {' '.join(pytest_options)} {TEST_DIR} {SOURCE_DIR}")


@task(
    help={
        "fmt": "Build a local report: report, html, json, annotate, html, xml.",
        "open_browser": "Open the coverage report in the web browser (requires --fmt html)",
    }
)
def coverage(c, fmt="report", open_browser=False):
    # type: (Context, str, bool) -> None
    """Create coverage report."""
    if any(Path().glob(".coverage.*")):
        _run(c, "coverage combine")
    _run(c, "coverage report -i")
    if fmt != "report":
        _run(c, f"coverage {fmt} -i")
    if fmt == "html" and open_browser:
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task(pre=[hooks, mypy, pylint, docs, safety, tests, coverage, doctest])
def check(c):
    # type: (Context) -> None
    """Run all checks together."""


@task(
    help={  # noqa
        "part": "Part of the version to be bumped.",
        "dry_run": "Don't write any files, just pretend. (default: False)",
        "allow_dirty": "Normally, bumpversion will abort if the working directory is "
        "dirty to protect yourself from releasing unversioned files and/or "
        "overwriting unsaved changes. Use this option to override this check.",
    }
)
def version(c, part, dry_run=False, allow_dirty=False):
    # type: (Context, str, bool, bool) -> None
    """Bump version."""
    bump_options = []
    if dry_run:
        bump_options.append("--dry-run")
    if allow_dirty:
        bump_options.append("--allow-dirty")
    _run(c, f"bump2version {' '.join(bump_options)} {part}")
