"""Tests for the `narrow_down.sqlite` module."""
import pytest

import narrow_down.sqlite


@pytest.mark.asyncio
async def test_sqlite_store__init__already_exists(tmp_path):
    dbfile = str(tmp_path / "test.db")
    await narrow_down.sqlite.SQLiteStore(dbfile).initialize()
    with pytest.raises(narrow_down.data_types.AlreadyInitialized):
        await narrow_down.sqlite.SQLiteStore(dbfile).initialize()


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__no_id(tmp_path):
    ims = await narrow_down.sqlite.SQLiteStore(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__duplicate_doc(tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    ims = await narrow_down.sqlite.SQLiteStore(str(tmp_path / "test.db")).initialize()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id(tmp_path):
    ims = await narrow_down.sqlite.SQLiteStore(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id_duplicate(tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    ims = await narrow_down.sqlite.SQLiteStore(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query(tmp_path):
    ims = await narrow_down.sqlite.SQLiteStore(str(tmp_path / "test.db")).initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]
