"""Tests for the `narrow_down.sqlite` and  `narrow_down.async_sqlite` modules."""

import pytest

import narrow_down.sqlite


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_setting():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_sqlite_store__query_setting__uninitialized():
    ims = narrow_down.sqlite.SQLiteStore(":memory:")
    assert await ims.query_setting("k") is None


@pytest.mark.asyncio
async def test_sqlite_store__query_setting__not_in():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    assert await ims.query_setting("k") is None


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__overwrite():
    """Adding a duplicate before to see if that's also handled."""
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    await ims.insert_setting(key="k", value="155")
    await ims.insert_setting(key="k", value="268")
    assert await ims.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__close_and_reopen(tmp_path):
    """Adding a duplicate before to see if that's also handled."""
    filename = str(tmp_path / "test.db")

    async def insert_setting():
        store = await narrow_down.sqlite.SQLiteStore(filename).initialize()
        await store.insert_setting(key="k", value="155")

    await insert_setting()

    store2 = narrow_down.sqlite.SQLiteStore(filename)
    assert await store2.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_sqlite_store__init__already_exists(tmp_path):
    dbfile = str(tmp_path / "test.db")
    await narrow_down.sqlite.SQLiteStore(dbfile).initialize()
    ims = await narrow_down.sqlite.SQLiteStore(dbfile).initialize()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__no_id():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__reopen(tmp_path):
    dbfile = str(tmp_path / "test.db")

    async def insert_doc():
        store = await narrow_down.sqlite.SQLiteStore(dbfile).initialize()
        return await store.insert_document(document=b"abcd efgh")

    id_out = await insert_doc()
    store2 = narrow_down.sqlite.SQLiteStore(dbfile)
    assert await store2.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__duplicate_doc():
    """Adding a duplicate before to see if that's also handled."""
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__insert_query_document__given_id_duplicate():
    """Adding a duplicate before to see if that's also handled."""
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query__reopen(tmp_path):
    dbfile = str(tmp_path / "test.db")

    async def insert_doc():
        store = await narrow_down.sqlite.SQLiteStore(dbfile).initialize()
        await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    await insert_doc()
    store2 = narrow_down.sqlite.SQLiteStore(dbfile)
    assert list(await store2.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]


@pytest.mark.asyncio
async def test_sqlite_store__remove_document__given_id():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"
    await ims.remove_document(id_out)
    with pytest.raises(KeyError):
        await ims.query_document(id_out)


@pytest.mark.asyncio
async def test_sqlite_store__remove_documents_from_bucket_and_query():
    ims = await narrow_down.sqlite.SQLiteStore(":memory:").initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]


@pytest.mark.parametrize("partitions", [1, 3, 100])
@pytest.mark.asyncio
async def test_sqlite_store__add_documents_to_bucket_and_query__custom_partitions(partitions):
    ims = await narrow_down.sqlite.SQLiteStore(":memory:", partitions=partitions).initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.parametrize("partitions", [1, 3, 100])
@pytest.mark.asyncio
async def test_sqlite_store__remove_documents_from_bucket__custom_partitions(partitions):
    ims = await narrow_down.sqlite.SQLiteStore(":memory:", partitions=partitions).initialize()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]


@pytest.mark.parametrize("partitions", [1, 3, 100])
@pytest.mark.asyncio
async def test_sqlite_store__custom_partitions_after_reopening(tmp_path, partitions):
    dbfile = str(tmp_path / "test.db")

    async def insert_doc():
        store = await narrow_down.sqlite.SQLiteStore(dbfile, partitions=partitions).initialize()
        assert store.partitions == partitions
        await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    await insert_doc()
    store2 = narrow_down.sqlite.SQLiteStore(dbfile)
    assert store2.partitions == partitions
    assert list(await store2.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
