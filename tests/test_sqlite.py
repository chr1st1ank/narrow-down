"""Tests for the `narrow_down.sqlite` and  `narrow_down.async_sqlite` modules."""
from typing import Type

import pytest

import narrow_down.sqlite


@pytest.fixture()
def sqlite_driver() -> Type[narrow_down.storage.StorageBackend]:
    return narrow_down.sqlite.SQLiteStore


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_setting(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_sqlite_store__query_setting__uninitialized(sqlite_driver, tmp_path):
    ims = sqlite_driver(str(tmp_path / "test.db"))
    assert await ims.query_setting("k") is None


@pytest.mark.asyncio
async def test_sqlite_store__query_setting__not_in(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    assert await ims.query_setting("k") is None


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__overwrite(sqlite_driver, tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    await ims.insert_setting(key="k", value="155")
    await ims.insert_setting(key="k", value="268")
    assert await ims.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__close_and_reopen(sqlite_driver, tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    filename = str(tmp_path / "test.db")

    async def insert_setting():
        store = await sqlite_driver(filename).initialize()
        await store.insert_setting(key="k", value="155")

    await insert_setting()

    store2 = sqlite_driver(filename)
    assert await store2.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_sqlite_store__init__already_exists(sqlite_driver, tmp_path):
    dbfile = str(tmp_path / "test.db")
    await sqlite_driver(dbfile).initialize()
    with pytest.raises(narrow_down.data_types.AlreadyInitialized):
        await sqlite_driver(dbfile).initialize()


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__no_id(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__reopen(sqlite_driver, tmp_path):
    dbfile = str(tmp_path / "test.db")

    async def insert_doc():
        store = await sqlite_driver(dbfile).initialize()
        return await store.insert_document(document=b"abcd efgh")

    id_out = await insert_doc()
    store2 = sqlite_driver(dbfile)
    assert await store2.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__duplicate_doc(sqlite_driver, tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id_duplicate(sqlite_driver, tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query__reopen(sqlite_driver, tmp_path):
    dbfile = str(tmp_path / "test.db")

    async def insert_doc():
        store = await sqlite_driver(dbfile).initialize()
        await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    await insert_doc()
    store2 = sqlite_driver(dbfile)
    assert list(await store2.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]


@pytest.mark.asyncio
async def test_sqlite_store__remove_document__given_id(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"
    await ims.remove_document(id_out)
    with pytest.raises(KeyError):
        await ims.query_document(id_out)


@pytest.mark.asyncio
async def test_sqlite_store__remove_documents_to_bucket_and_query(sqlite_driver, tmp_path):
    ims = await sqlite_driver(str(tmp_path / "test.db")).initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]
