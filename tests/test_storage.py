"""Tests for the `narrow_down.storage` module."""
import pytest

import narrow_down.storage


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_setting():
    ims = narrow_down.storage.InMemoryStore()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__overwrite():
    """Adding a duplicate before to see if that's also handled."""
    ims = narrow_down.storage.InMemoryStore()
    await ims.insert_setting(key="k", value="155")
    await ims.insert_setting(key="k", value="268")
    assert await ims.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__no_id():
    ims = narrow_down.storage.InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__duplicate_doc():
    """Adding a duplicate before to see if that's also handled."""
    ims = narrow_down.storage.InMemoryStore()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id():
    ims = narrow_down.storage.InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id="12 34")
    assert id_out == "12 34"
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id_duplicate():
    """Adding a duplicate before to see if that's also handled."""
    ims = narrow_down.storage.InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id="12 34")
    assert id_out == "12 34"
    id_out = await ims.insert_document(document=b"abcd efgh", document_id="12 34")
    assert id_out == "12 34"
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__add_documents_to_bucket_and_query():
    ims = narrow_down.storage.InMemoryStore()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id="10")
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id="20")
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id="21")
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == ["10"]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == ["20", "21"]
