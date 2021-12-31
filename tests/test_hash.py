"""Tests for `narrow_down.hash`."""
from narrow_down import hash


def test_murmur_rust():
    import murmurhash.mrmr

    assert murmurhash.mrmr.hash("abcd".encode("utf-8")) == hash.murmur3_32bit("abcd")
