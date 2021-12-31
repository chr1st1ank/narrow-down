"""Tests for `narrow_down.hash`."""
from narrow_down import hash


def test_murmur3_32bit():
    assert hash.murmur3_32bit("test") == 3127628307
    assert hash.murmur3_32bit("") == 0


def test_xxhash_32bit():
    assert hash.xxhash_32bit("test") == 1042293711
    assert hash.xxhash_32bit("") == 46947589


def test_xxhash_64bit():
    assert hash.xxhash_64bit("test") == 5754696928334414137
    assert hash.xxhash_64bit("") == 17241709254077376921
