"""Tests for `narrow_down.similarity_store`."""
import pytest

import narrow_down.data_types
from narrow_down.data_types import StorageLevel
from narrow_down.similarity_store import SimilarityStore


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Document,
        StorageLevel.Full,
    ],
)
async def test_similarity_store__insert_and_query_with_default_settings(storage_level):
    simstore = SimilarityStore(storage_level=storage_level)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id

    if storage_level & StorageLevel.Document:
        assert list(results)[0].document == sample_doc
    else:
        assert list(results)[0].document is None


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id():
    simstore = SimilarityStore(storage_level=StorageLevel.Fingerprint)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    await simstore.remove_by_id(doc_id)
    await simstore.remove_by_id(doc_id + 1, check_if_exists=False)
    results = await simstore.query(sample_doc)

    assert list(results) == []


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__error_storage_level():
    simstore = SimilarityStore(storage_level=StorageLevel.Minimal)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(narrow_down.data_types.TooLowStorageLevel):
        await simstore.remove_by_id(doc_id)
    results = await simstore.query(sample_doc)

    assert len(results) == 1


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__key_error():
    simstore = SimilarityStore(storage_level=StorageLevel.Fingerprint)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(KeyError):
        await simstore.remove_by_id(doc_id + 1, check_if_exists=True)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
