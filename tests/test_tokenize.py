"""Tests for `narrow_down.tokenize`."""

import pytest

from narrow_down import tokenize


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, ""), (2, "")])
def test_char_ngrams__str_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.char_ngrams("", **kwargs) == set()


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, b""), (2, b"")])
def test_char_ngrams__bytes_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.char_ngrams("", **kwargs) == set()


@pytest.mark.parametrize(
    "s, n, pad_char, expected",
    [
        ("a", 1, None, {"a"}),
        ("abac", 1, None, {"a", "b", "c"}),
        ("abac", 2, None, {"ba", "c$", "ab", "ac", "$a"}),
        ("a", 1, "", {"a"}),
        ("abac", 1, "", {"a", "b", "c"}),
        ("abac", 2, "", {"ac", "ab", "ba"}),
        ("a", 1, "#", {"a"}),
        ("abac", 1, "#", {"a", "b", "c"}),
        ("abac", 2, "#", {"ba", "ab", "c#", "#a", "ac"}),
    ],
)
def test_char_ngrams__str(s, n, pad_char, expected):
    """Check the results for normal use."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.char_ngrams(s, **kwargs) == expected


@pytest.mark.parametrize(
    "s, n, pad_char, expected",
    [
        (b"a", 1, b"", {b"a"}),
        (b"abac", 1, b"", {b"a", b"b", b"c"}),
        (b"abac", 2, b"", {b"ac", b"ab", b"ba"}),
        (b"a", 1, b"#", {b"a"}),
        (b"abac", 1, b"#", {b"a", b"b", b"c"}),
        (b"abac", 2, b"#", {b"ba", b"ab", b"c#", b"#a", b"ac"}),
    ],
)
def test_char_ngrams__bytes(s, n, pad_char, expected):
    """Check the results for normal use."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.char_ngrams(s, **kwargs) == expected


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, ""), (2, "")])
def test_count_char_ngrams__str_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.count_char_ngrams("", **kwargs) == {}


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, b""), (2, b"")])
def test_count_char_ngrams__bytes_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.count_char_ngrams("", **kwargs) == {}


@pytest.mark.parametrize(
    "s, n, pad_char, expected",
    [
        ("a", 1, None, {"a": 1}),
        ("abac", 1, None, {"a": 2, "b": 1, "c": 1}),
        ("abac", 2, None, {"$a": 1, "ab": 1, "ba": 1, "ac": 1, "c$": 1}),
        ("a", 1, "", {"a": 1}),
        ("abac", 1, "", {"a": 2, "b": 1, "c": 1}),
        ("abac", 2, "", {"ab": 1, "ba": 1, "ac": 1}),
        ("a", 1, "#", {"a": 1}),
        ("abac", 1, "#", {"a": 2, "b": 1, "c": 1}),
        ("abac", 2, "#", {"#a": 1, "ab": 1, "ba": 1, "ac": 1, "c#": 1}),
    ],
)
def test_count_char_ngrams__str(s, n, pad_char, expected):
    """Check the results for normal use."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.count_char_ngrams(s, **kwargs) == expected


@pytest.mark.parametrize(
    "s, n, pad_char, expected",
    [
        (b"a", 1, b"", {b"a": 1}),
        (b"abac", 1, b"", {b"a": 2, b"b": 1, b"c": 1}),
        (b"abac", 2, b"", {b"ab": 1, b"ba": 1, b"ac": 1}),
        (b"a", 1, b"#", {b"a": 1}),
        (b"abac", 1, b"#", {b"a": 2, b"b": 1, b"c": 1}),
        (b"abac", 2, b"#", {b"#a": 1, b"ab": 1, b"ba": 1, b"ac": 1, b"c#": 1}),
    ],
)
def test_count_char_ngrams__bytes(s, n, pad_char, expected):
    """Check the results for normal use."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert tokenize.count_char_ngrams(s, **kwargs) == expected
