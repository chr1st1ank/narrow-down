"""Tests for `narrow_down._tokenize`."""
# pylint: disable=use-dict-literal

import pytest

from narrow_down import _tokenize


@pytest.mark.parametrize(
    "s, n, expected",
    [
        ("", 1, set()),
        ("two words", 1, {"two", "words"}),
        (" two  words ", 1, {"two", "words"}),
        ("\ttwo\nwords", 1, {"two", "words"}),
        ("two\twords", 1, {"two", "words"}),
        ("two words", 2, {"two words"}),
        (" two  words ", 2, {"two words"}),
        ("\ttwo\nwords", 2, {"two words"}),
        ("two\twords", 2, {"two words"}),
        ("two words", 3, {"two words"}),
        ("three words long", 2, {"three words", "words long"}),
    ],
)
def test_word_ngrams(s, n, expected):
    assert _tokenize.word_ngrams(s, n) == expected


@pytest.mark.parametrize("n", [1, 3, 5])
def test_word_ngrams__benchmark(benchmark, sample_sentences_french, n):
    def f():
        for s in sample_sentences_french:
            _tokenize.word_ngrams(s, n)
        return _tokenize.word_ngrams(
            "De 1990 à 2000, ce fut Théodore Mel Eg avec deux mandats également.", n
        )

    tokens = benchmark(f)
    # fmt: off
    if n == 1:
        assert tokens == {
            "De", "1990", "à", "2000,", "ce", "fut", "Théodore",
            "Mel", "Eg", "avec", "deux", "mandats", "également.",
        }
    elif n == 3:
        assert tokens == {
            "De 1990 à", "1990 à 2000,", "à 2000, ce", "2000, ce fut",
            "ce fut Théodore", "fut Théodore Mel", "Théodore Mel Eg",
            "Mel Eg avec", "Eg avec deux", "avec deux mandats", "deux mandats également.",
        }
    # fmt: on


@pytest.mark.parametrize("n", [1, 3, 5])
def test_char_ngrams__str__benchmark(benchmark, sample_sentences_french, n):
    def f():
        for s in sample_sentences_french:
            _tokenize.char_ngrams(s, n)
        return _tokenize.char_ngrams(
            "De 1990 à 2000, ce fut Théodore Mel Eg avec deux mandats également.", n
        )

    tokens = benchmark(f)
    # fmt: off
    if n == 1:
        assert tokens == {
            '9', 'a', 'T', 'h', 'f', 'u', 'e', 'E', ' ', '1', 'g', '2', 'D', 'm', 's',
            'M', 'd', 'é', 'v', '0', 't', 'r', 'x', 'n', 'l', 'à', ',', 'o', 'c', '.'
        }
    elif n == 3:
        assert tokens == {
            'c d', 'gal', 'e M', 'fut', 'De ', ' fu', 'éga', 'ent', ', c', ' Th', 'ave',
            '90 ', '0, ', 'ats', 'ux ', 'and', 'Eg ', 'e 1', '$De', ' à ', 'e f', 'x m',
            'nda', '$$D', 'éod', 'ce ', ' ce', ' 20', 't.$', ' 19', '990', 't T', 'nt.',
            'l E', 'à 2', ' av', ' ég', 'ec ', 'lem', 're ', 'dor', ' ma', ' Eg', 'el ',
            'g a', 'odo', 'ts ', 'men', 'vec', '200', 'ore', '0 à', ' Me', '000', 'eux',
            '.$$', 'eme', 's é', '199', '00,', 'ut ', 'deu', 'Thé', 'ale', 'dat', ' de',
            'héo', 'man', 'Mel'
        }
    # fmt: on


def test_char_ngrams__bytes__benchmark(benchmark):
    """Check the results for normal use."""
    testdata = [
        (b"a", 1, b"", {b"a"}),
        (b"abac", 1, b"", {b"a", b"b", b"c"}),
        (b"abac", 2, b"", {b"ac", b"ab", b"ba"}),
        (b"a", 1, b"#", {b"a"}),
        (b"abac", 1, b"#", {b"a", b"b", b"c"}),
        (b"abac", 2, b"#", {b"ba", b"ab", b"c#", b"#a", b"ac"}),
    ]

    def f():
        for s, n, pad_char, _ in testdata:
            _tokenize.char_ngrams(s, n, pad_char)
        return _tokenize.char_ngrams(s, n, pad_char)

    tokens = benchmark(f)
    assert tokens == testdata[-1][-1]


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, ""), (2, "")])
def test_char_ngrams__str_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert _tokenize.char_ngrams("", **kwargs) == set()


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, b""), (2, b"")])
def test_char_ngrams__bytes_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert _tokenize.char_ngrams("", **kwargs) == set()


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
    assert _tokenize.char_ngrams(s, **kwargs) == expected


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
    assert _tokenize.char_ngrams(s, **kwargs) == expected


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, ""), (2, "")])
def test_count_char_ngrams__str_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert _tokenize.count_char_ngrams("", **kwargs) == {}


@pytest.mark.parametrize("n, pad_char", [(1, None), (2, None), (1, b""), (2, b"")])
def test_count_char_ngrams__bytes_empty_string(n, pad_char):
    """For an empty input the output should always be empty."""
    kwargs = {k: v for k, v in dict(n=n, pad_char=pad_char).items() if v is not None}
    assert _tokenize.count_char_ngrams("", **kwargs) == {}


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
    assert _tokenize.count_char_ngrams(s, **kwargs) == expected


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
    assert _tokenize.count_char_ngrams(s, **kwargs) == expected
