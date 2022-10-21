"""Tests for `narrow_down.hash`."""
import pytest

from narrow_down import hash as hash_


def test_murmur3_32bit():
    assert hash_.murmur3_32bit("test".encode("utf-8")) == 3127628307
    assert hash_.murmur3_32bit("".encode("utf-8")) == 0


def test_xxhash_32bit():
    assert hash_.xxhash_32bit("test".encode("utf-8")) == 1042293711
    assert hash_.xxhash_32bit("".encode("utf-8")) == 46947589


def test_xxhash_64bit():
    assert hash_.xxhash_64bit("test".encode("utf-8")) == 5754696928334414137
    assert hash_.xxhash_64bit("".encode("utf-8")) == 17241709254077376921


@pytest.mark.parametrize(
    "hashfunction", [hash_.murmur3_32bit, hash_.xxhash_32bit, hash_.xxhash_64bit]
)
def test_hashfunction_benchmark(benchmark, sample_byte_strings, hashfunction):
    def f():
        return list(map(hashfunction, sample_byte_strings))[-1]

    result = benchmark(f)

    assert isinstance(result, int)
