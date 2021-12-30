"""Tests for `narrow_down.__init__` module."""

import re

import narrow_down


def test_version() -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    assert re.match(r"\d(\.\d)*(-[\w\.]+)?", narrow_down.__version__)
