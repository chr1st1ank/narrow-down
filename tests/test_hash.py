"""Tests for `narrow_down.hash`."""
import pytest

from narrow_down import hash


def test_murmur3_32bit():
    assert hash.murmur3_32bit("test".encode("utf-8")) == 3127628307
    assert hash.murmur3_32bit("".encode("utf-8")) == 0


def test_xxhash_32bit():
    assert hash.xxhash_32bit("test".encode("utf-8")) == 1042293711
    assert hash.xxhash_32bit("".encode("utf-8")) == 46947589


def test_xxhash_64bit():
    assert hash.xxhash_64bit("test".encode("utf-8")) == 5754696928334414137
    assert hash.xxhash_64bit("".encode("utf-8")) == 17241709254077376921


SAMPLE_BYTE_STRINGS = [
    b"QHtbc3lzdGVtICJ0b3VjaCAvdG1wL2JsbnMuZmFpbCJdfQ==",
    b"ZXZhbCgicHV0cyAnaGVsbG8gd29ybGQnIik=",
    b"U3lzdGVtKCJscyAtYWwgLyIp",
    b"YGxzIC1hbCAvYA==",
    b"S2VybmVsLmV4ZWMoImxzIC1hbCAvIik=",
    b"S2VybmVsLmV4aXQoMSk=",
    b"JXgoJ2xzIC1hbCAvJyk=",
    b"PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iSVNPLTg4NTktMSI/PjwhRE9DVFlQRSBmb28g",
    b"WyA8IUVMRU1FTlQgZm9vIEFOWSA+PCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFz",
    b"c3dkIiA+XT48Zm9vPiZ4eGU7PC9mb28+",
    b"JEhPTUU=",
    b"JEVOVnsnSE9NRSd9",
    b"true",
    b"false",
    b"-1.00",
    b"-$1.00",
    b"-1/2",
    b"-1E2",
    b"0/0",
    b"-2147483648/-1",
    b"-9223372036854775808/-1",
    b"-0",
    b"-0.0",
    b"+0",
    b"+0.0",
]


@pytest.mark.parametrize("hashfunction", [hash.murmur3_32bit, hash.xxhash_32bit, hash.xxhash_64bit])
def test_hashfunction_benchmark(benchmark, hashfunction):
    def f():
        return list(map(hashfunction, SAMPLE_BYTE_STRINGS))[-1]

    result = benchmark(f)

    assert isinstance(result, int)
