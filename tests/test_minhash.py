"""Tests for `narrow_down.minhash`."""
import numpy as np
import pytest

from narrow_down import _minhash, storage
from narrow_down.storage import StorageLevel, StoredDocument, TooLowStorageLevel


def test_minhash_lsh_config__json():
    config1 = _minhash.MinhashLshConfig(0, 1, 2)
    assert _minhash.MinhashLshConfig.from_json(config1.to_json()) == config1


def test_minhash():
    """Check minhashing of a document with hand-checked result."""
    mh = _minhash.MinHasher(2, 42)
    minhashes = mh.minhash(["abc", "def", "g"])

    assert minhashes.shape == (2,)
    assert minhashes.dtype == np.uint32
    assert (minhashes == np.array([2048153058, 2194504465], dtype=np.uint32)).all()


def test_minhash_benchmark(benchmark, sample_byte_strings):
    sample_strings = [s.decode("utf-8") for s in sample_byte_strings]

    def f():
        mh = _minhash.MinHasher(64, 42)
        return list(map(mh.minhash, sample_strings))[-1]

    minhashes = benchmark(f)

    assert minhashes.dtype == np.uint32
    assert minhashes.shape == (64,)


@pytest.mark.asyncio
async def test_lsh__basic_lookup_without_exact_part():
    """Minimal check if an LSH can be constructed."""
    test_doc = StoredDocument(
        exact_part="exact:part",
        fingerprint=storage.Fingerprint(np.array([2 * i for i in range(1, 22)])),
    )
    unrelated_doc = StoredDocument(
        exact_part="exact:part",
        fingerprint=storage.Fingerprint(np.array([3 * i for i in range(0, 21)])),
    )
    lsh = _minhash.LSH(
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
    )
    await lsh.insert(test_doc.without("exact_part"))
    await lsh.insert(unrelated_doc.without("exact_part"))
    result = await lsh.query(test_doc.fingerprint)
    print(result)
    assert len(result) == 1
    assert (list(result)[0].fingerprint == test_doc.fingerprint).all


@pytest.mark.asyncio
async def test_lsh__basic_lookup_with_exact_part():
    """Minimal check if an LSH can be constructed."""
    test_doc = StoredDocument(
        # document="abc def",
        exact_part="exact:part",
        # data="some custom payload",
        fingerprint=storage.Fingerprint(np.array([2, 4, 6])),
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
async def test_lsh__top_n():
    """Minimal check if an LSH can be constructed."""
    lsh = _minhash.LSH(
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
    )
    await lsh.insert(
        StoredDocument(document="1", fingerprint=storage.Fingerprint(np.array([2, 4, 6]))),
    )
    await lsh.insert(
        StoredDocument(document="2", fingerprint=storage.Fingerprint(np.array([2, 4, 7]))),
    )
    await lsh.insert(
        StoredDocument(document="3", fingerprint=storage.Fingerprint(np.array([2, 5, 7]))),
    )
    await lsh.insert(
        StoredDocument(document="4", fingerprint=storage.Fingerprint(np.array([3, 5, 7]))),
    )

    result = await lsh.query_top_n(n=1, fingerprint=storage.Fingerprint(np.array([2, 4, 6])))
    print(result)
    assert sorted([r.document for r in result]) == ["1"]

    result = await lsh.query_top_n(n=2, fingerprint=storage.Fingerprint(np.array([2, 4, 6])))
    print(result)
    assert sorted([r.document for r in result]) == ["1", "2"]

    result = await lsh.query_top_n(n=3, fingerprint=storage.Fingerprint(np.array([2, 4, 6])))
    print(result)
    assert sorted([r.document for r in result]) == ["1", "2", "3"]

    result = await lsh.query_top_n(n=4, fingerprint=storage.Fingerprint(np.array([2, 4, 6])))
    print(result)
    assert sorted([r.document for r in result]) == ["1", "2", "3"]


@pytest.mark.asyncio
async def test_lsh__insert_invalid_document():
    """Test error handling of insert()."""
    lsh = _minhash.LSH(_minhash.MinhashLshConfig(1, 1, 1), None)
    with pytest.raises(ValueError):
        await lsh.insert(StoredDocument())


@pytest.mark.asyncio
async def test_lsh__remove_by_id():
    """Try to remove a document from the index."""
    f = storage.Fingerprint(np.array([2, 4, 6]))
    test_doc = StoredDocument(fingerprint=f)
    lsh = _minhash.LSH(
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
    )
    index = await lsh.insert(test_doc)
    await lsh.remove_by_id(index, check_if_exists=True)
    assert list(await lsh.query(f)) == []


@pytest.mark.asyncio
async def test_lsh__remove_by_id__missing_fingerprint():
    """Try to remove a document from the index when the storage level is too low."""
    f = storage.Fingerprint(np.array([2, 4, 6]))
    test_doc = StoredDocument(fingerprint=f)
    lsh = _minhash.LSH(
        _minhash.MinhashLshConfig(n_hashes=2, n_bands=2, rows_per_band=1),
        storage=await storage.InMemoryStore().initialize(),
    )
    index = await lsh.insert(test_doc, storage_level=StorageLevel.Minimal)
    with pytest.raises(TooLowStorageLevel):
        await lsh.remove_by_id(index, check_if_exists=True)


@pytest.mark.parametrize(
    "j, fn, fp, expected",
    [
        (0.5, 0.05, 0.05, _minhash.MinhashLshConfig(n_hashes=128, n_bands=22, rows_per_band=5)),
        (0.5, 1, 0.1, _minhash.MinhashLshConfig(n_hashes=16, n_bands=1, rows_per_band=16)),
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
