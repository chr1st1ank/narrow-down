"""Tests for the `narrow_down.scylladb` module."""

import cassandra.cluster  # type: ignore
import pytest

import narrow_down.scylladb


@pytest.fixture
def scylladb_cluster():
    return cassandra.cluster.Cluster(
        contact_points=["localhost"], port=9042, cql_version="3.3.1", protocol_version=4
    )


def recreate_keyspace(cluster, name):
    with cluster.connect() as session:
        session.execute(f"DROP KEYSPACE IF EXISTS {name};")
        session.execute(
            f"CREATE KEYSPACE IF NOT EXISTS {name} "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1} "
            "AND durable_writes = False"
        )


@pytest.mark.asyncio
async def test_scylladb_store__initialize(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "initialize")
    storage = narrow_down.scylladb.ScyllaDBStore(scylladb_cluster, "initialize")
    await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__initialize_session(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "initialize")
    with scylladb_cluster.connect() as session:
        storage = narrow_down.scylladb.ScyllaDBStore(session, "initialize")
        await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_setting(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "insert_query_setting")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_setting"
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    assert await storage.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_scylladb_store__query_missing_setting(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "query_missing_setting")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "query_missing_setting"
    ).initialize()
    assert await storage.query_setting("y") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__uninitialized(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "query_setting__uninitialized")
    storage = narrow_down.scylladb.ScyllaDBStore(scylladb_cluster, "query_setting__uninitialized")
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__not_in(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "query_setting__not_in")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "query_setting__not_in"
    ).initialize()
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__overwrite(scylladb_cluster):
    """Adding a duplicate before to see if that's also handled."""
    recreate_keyspace(scylladb_cluster, "insert_query_document__overwrite")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_document__overwrite"
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    await storage.insert_setting(key="k", value="268")
    assert await storage.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__no_id(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "insert_query_document__no_id")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_document__no_id"
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__duplicate_doc(scylladb_cluster):
    """Adding a duplicate before to see if that's also handled."""
    recreate_keyspace(scylladb_cluster, "insert_query_document__duplicate_doc")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_document__duplicate_doc"
    ).initialize()
    await storage.insert_document(document=b"abcd efgh")
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "insert_query_document__given_id")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_document__given_id"
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id_duplicate(scylladb_cluster):
    """Adding a duplicate before to see if that's also handled."""
    recreate_keyspace(scylladb_cluster, "insert_query_document__given_id_duplicate")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "insert_query_document__given_id_duplicate"
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__add_documents_to_bucket_and_query(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "add_documents_to_bucket_and_query")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "add_documents_to_bucket_and_query"
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await storage.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_scylladb_store__remove_document__given_id(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "remove_document__given_id")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "remove_document__given_id"
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"
    await storage.remove_document(id_out)
    with pytest.raises(KeyError):
        await storage.query_document(id_out)


@pytest.mark.asyncio
async def test_scylladb_store__remove_documents_to_bucket_and_query(scylladb_cluster):
    recreate_keyspace(scylladb_cluster, "remove_documents_to_bucket_and_query")
    storage = await narrow_down.scylladb.ScyllaDBStore(
        scylladb_cluster, "remove_documents_to_bucket_and_query"
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]
    await storage.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]
