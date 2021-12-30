"""Tests for `narrow_down` module."""
from typing import Generator

import pytest

import narrow_down


@pytest.fixture
def version() -> Generator[str, None, None]:
    """Sample pytest fixture."""
    yield narrow_down.__version__


def test_version(version: str) -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    assert version == "0.1.0"
