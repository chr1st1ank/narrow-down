"""Tests for `narrow_down.minhash`."""
import numpy as np
import pytest

from narrow_down import _minhash, data_types, storage


def test_minhash():
    """Check minhashing of a document with hand-checked result."""
    mh = _minhash.MinHasher(2, 42)
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
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
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
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
    )
    await lsh.insert(test_doc.fingerprint, exact_part=test_doc.exact_part)
    result = await lsh.query(test_doc.fingerprint, exact_part=test_doc.exact_part)
    print(result)
    assert len(result) == 1
    assert (list(result)[0].fingerprint == test_doc.fingerprint).all
    assert list(result)[0].exact_part == test_doc.exact_part


@pytest.mark.parametrize(
    "j, fn, fp, expected",
    [(0.5, 0.05, 0.05, _minhash.MinhashLshConfig(n_hashes=128, n_bands=22, rows_per_band=5))],
)
def test_find_optimal_config(j, fn, fp, expected):
    assert (
        _minhash.find_optimal_config(
            jaccard_threshold=j, max_false_negative_proba=fn, max_false_positive_proba=fp
        )
        == expected
    )
