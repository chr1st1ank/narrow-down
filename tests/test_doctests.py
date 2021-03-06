"""Run doctest on all docstrings of the package."""
import doctest
import importlib
import pkgutil
from pathlib import Path

import pytest

import narrow_down

REPOSITORY_ROOT = Path(__file__).parent.parent


def modules_in_package(package):
    """Find and import all modules in the given package."""
    backlog = [package]
    modules = []
    while backlog:
        current_package = backlog.pop()
        modules.append(current_package)
        for _, modname, ispkg in pkgutil.iter_modules(current_package.__path__):
            if ispkg:
                backlog.append(importlib.import_module(f"{current_package.__name__}.{modname}"))
            else:
                modules.append(importlib.import_module(f"{current_package.__name__}.{modname}"))
    return modules


@pytest.mark.parametrize("module", modules_in_package(narrow_down))
def test_package_doctest(module):
    """Run a module's doctests."""
    try:
        doctest.testmod(module, raise_on_error=True, verbose=True)
    except doctest.DocTestFailure as f:
        print(f"Got:\n    {f.got}")
        raise


@pytest.fixture(
    params=REPOSITORY_ROOT.glob("docs/*.md"),
    ids=lambda p: str(p.relative_to(REPOSITORY_ROOT)),
)
def docfile(request):
    """Return all documentation files with Python code to be tested."""
    return request.param


def test_doc_snippets_doctest(docfile):
    """Run the python snippets in the documentation."""
    doctest.testfile(
        str((REPOSITORY_ROOT / docfile).absolute()),
        module_relative=False,
        raise_on_error=True,
        verbose=True,
        optionflags=doctest.NORMALIZE_WHITESPACE,
    )
