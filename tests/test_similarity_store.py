"""Tests for `narrow_down.similarity_store`."""
import pytest

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
