"""Tests for `narrow_down.minhash`."""
import numpy as np
import pytest

from narrow_down import _minhash, data_types, hash, storage


def test_minhash():
    """Check minhashing of a document with hand-checked result."""
    mh = _minhash.MinHasher(hash.HashAlgorithm.Murmur3_32bit, 2, 42)
    minhashes = mh.minhash(["abc", "def", "g"])

    assert minhashes.shape == (2,)
    assert minhashes.dtype == np.uint32
    assert (minhashes == np.array([530362422, 32829942], dtype=np.uint32)).all()


@pytest.mark.asyncio
async def test_lsh__basic_lookup_without_exact_part():
    """Minimal check if an LSH can be constructed."""
    test_doc = data_types.StoredDocument(
        # document="abc def",
        exact_part="exact:part",
        # data="some custom payload",
        fingerprint=data_types.Fingerprint(np.array([2, 4, 6])),
    )
    lsh = _minhash.LSH(
        2, 2, hash.HashAlgorithm.Murmur3_32bit, await storage.InMemoryStore().initialize()
    )
    await lsh.insert(
        test_doc.fingerprint,
    )
    result = await lsh.query(test_doc.fingerprint)
    print(result)
    assert len(result) == 1
    assert (list(result)[0].fingerprint == test_doc.fingerprint).all


@pytest.mark.asyncio
async def test_lsh__basic_lookup_with_exact_part():
    """Minimal check if an LSH can be constructed."""
    test_doc = data_types.StoredDocument(
        # document="abc def",
        exact_part="exact:part",
        # data="some custom payload",
        fingerprint=data_types.Fingerprint(np.array([2, 4, 6])),
    )
    lsh = _minhash.LSH(
        2, 2, hash.HashAlgorithm.Murmur3_32bit, await storage.InMemoryStore().initialize()
    )
    await lsh.insert(test_doc.fingerprint, exact_part=test_doc.exact_part)
    result = await lsh.query(test_doc.fingerprint, exact_part=test_doc.exact_part)
    print(result)
    assert len(result) == 1
    assert (list(result)[0].fingerprint == test_doc.fingerprint).all
    assert list(result)[0].exact_part == test_doc.exact_part
