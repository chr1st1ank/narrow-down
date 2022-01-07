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
    await lsh.insert(test_doc.without("exact_part"))
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
    await lsh.insert(test_doc)
    result = await lsh.query(test_doc.fingerprint, exact_part=test_doc.exact_part)
    print(result)
    assert len(result) == 1
    assert (list(result)[0].fingerprint == test_doc.fingerprint).all
    assert list(result)[0].exact_part == test_doc.exact_part


@pytest.mark.asyncio
async def test_lsh__insert_invalid_document():
    """Test error handling of insert()."""
    lsh = _minhash.LSH(_minhash.MinhashLshConfig(1, 1, 1), None)
    with pytest.raises(ValueError):
        await lsh.insert(data_types.StoredDocument())


@pytest.mark.parametrize(
    "j, fn, fp, expected",
    [
        (0.5, 0.05, 0.05, _minhash.MinhashLshConfig(n_hashes=128, n_bands=22, rows_per_band=5)),
        (0.5, 1, 0.1, _minhash.MinhashLshConfig(n_hashes=2, n_bands=1, rows_per_band=2)),
        (0.5, 0.1, 1, _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1)),
        (
            0.5,
            -1,
            0.2,
            _minhash.MinhashLshConfig(n_hashes=16384, n_bands=16384, rows_per_band=1),
        ),
        (
            0.5,
            1,
            -1,
            _minhash.MinhashLshConfig(n_hashes=16384, n_bands=1, rows_per_band=16384),
        ),
    ],
)
def test_find_optimal_config(j, fn, fp, expected) -> None:
    """Test the parameter optimization.

    Expectations: As long as the proba thresholds can't be reached the number of hashes should be
    increased. If the false negative threshold isn't reachable, the number of bands should be
    increased because that increases the matching chances. If the false positive threshold can't
    be reached the rows_per_band should be increased instead to reduce the matching chances.

    Args:
        j: Jaccard similarity threshold
        fn: Max false negative probability
        fp: Max false positive probabiblity
        expected: Expected output parameters
    """
    cfg = _minhash.find_optimal_config(
        jaccard_threshold=j, max_false_negative_proba=fn, max_false_positive_proba=fp
    )
    print(
        "False negative proba:",
        _minhash._false_negative_probability(j, b=cfg.n_bands, r=cfg.rows_per_band),
    )
    print(
        "False positive proba:",
        _minhash._false_positive_probability(j, b=cfg.n_bands, r=cfg.rows_per_band),
    )
    assert cfg == expected
