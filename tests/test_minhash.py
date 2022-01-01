"""Tests for `narrow_down.minhash`."""
import numpy as np

from narrow_down import hash, minhash


def test_minhash():
    """Check minhashing of a document with hand-checked result."""
    mh = minhash.MinHasher(hash.HashAlgorithm.Murmur3_32bit, 2, 42)
    minhashes = mh.minhash(["abc", "def", "g"])

    assert minhashes.shape == (2,)
    assert minhashes.dtype == np.uint32
    assert (minhashes == np.array([530362422, 32829942], dtype=np.uint32)).all()
