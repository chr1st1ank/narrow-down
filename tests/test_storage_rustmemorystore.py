"""Tests for RustMemoryStoreWrapper."""

import pytest

from narrow_down.storage import RustMemoryStoreWrapper


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_setting():
    ims = RustMemoryStoreWrapper()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__overwrite():
    """Adding a duplicate before to see if that's also handled."""
    ims = RustMemoryStoreWrapper()
    await ims.insert_setting(key="k", value="155")
    await ims.insert_setting(key="k", value="268")
    assert await ims.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__no_id():
    ims = RustMemoryStoreWrapper()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__duplicate_doc():
    """Adding a duplicate before to see if that's also handled."""
    ims = RustMemoryStoreWrapper()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id():
    ims = RustMemoryStoreWrapper()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id_duplicate():
    """Adding a duplicate before to see if that's also handled."""
    ims = RustMemoryStoreWrapper()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__add_documents_to_bucket_and_query():
    ims = RustMemoryStoreWrapper()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_in_memory_store__remove_documents_from_bucket():
    ims = RustMemoryStoreWrapper()

    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []

    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []

    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []
