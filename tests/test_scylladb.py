"""Tests for the `narrow_down.scylladb` module."""
import collections
import hashlib
import os
import re
from typing import Dict, List, NamedTuple, Tuple

import cassandra.cluster  # type: ignore
import cassandra.query  # type: ignore
import pytest

import narrow_down.scylladb

CONNECT_TO_DB = os.environ.get("TEST_WITH_DB", "False").lower() == "true"


class SessionMock:
    """Double and validating spy for a scylladb Session."""

    class _Result:
        """A mock Result object."""

        def __init__(self, content: List):
            self.content = content

        def __iter__(self):
            return self.content.__iter__()

        def all(self):  # noqa: A003  # We cannot choose a different name
            return [x for x in self]

        def one(self):
            return self.content[0]

    class _PreparedStament:
        """A mock object mimicking a PreparedStatement."""

        def __init__(self, query: str):
            self.query_string = query
            self.is_idempotent = False

    def __init__(self, real_session=None, keyspace=""):
        """Create a new Session object."""
        self.test_keyspace = keyspace
        self._real_session: cassandra.cluster.Session = real_session
        self._query_responses: Dict[str, List[collections.namedtuple]] = {}
        self._shutdown = False

    def add_mock_response(self, request: str, response: List[NamedTuple]):
        """Add an expected query with response list."""
        self._query_responses[request.replace("<keyspace>", self.test_keyspace)] = response

    def del_mock_response(self, request: str):
        """Remove one of the stored expected queries."""
        del self._query_responses[request.replace("<keyspace>", self.test_keyspace)]

    def prepare(self, query):
        """Create a prepared statement."""
        assert not self._shutdown
        if self._real_session:
            return self._real_session.prepare(query)
        return SessionMock._PreparedStament(query)

    def execute(self, query, parameters, timeout=1.0):
        """Run a query synchronously."""
        assert not self._shutdown
        query_string = self._prepare_query_string(query, parameters)

        if self._real_session:
            response = self._real_session.execute(query, parameters, timeout)
            assert response.all() == self._query_responses[query_string]
        return SessionMock._Result(self._query_responses[query_string])

    def execute_async(self, query, parameters, timeout=0.1):
        """Call session.execute() to run a query asynchronously."""
        assert not self._shutdown
        query_string = self._prepare_query_string(query, parameters)

        if self._real_session:
            future = self._real_session.execute_async(query, parameters, timeout)
            assert future.result().all() == self._query_responses.get(query_string)
            return future

        class FakeFuture:
            @staticmethod
            def add_callback(f):
                f(self._query_responses[query_string])

            @staticmethod
            def add_errback(f):
                pass

        return FakeFuture

    def _prepare_query_string(self, statement, parameters: Tuple):
        prepared = (
            re.sub(r"\s+", " ", statement.query_string)
            .replace("?", "{}")
            .format(*(parameters or []))
        )
        if prepared not in self._query_responses:
            expected_queries = ",\n  ".join(self._query_responses.keys())
            raise AssertionError(f"Unexpected query: {prepared}.\nExpecting:\n{expected_queries}")
        return prepared

    def __enter__(self):
        """Enter the session context as with cassandra.cluster.Session also possible."""
        return self

    def __exit__(self, *args):
        """Leave the context of the session and mark the session as closed."""
        self._shutdown = True


def row(**kwargs):
    return collections.namedtuple("Row", list(kwargs.keys()))(**kwargs)


@pytest.fixture(scope="function")
def scylladb_cluster():
    if not CONNECT_TO_DB:
        return None
    else:
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


@pytest.fixture(scope="function")
def session_mock(request, scylladb_cluster):
    keyspace_name = (
        request.node.name[-20:]
        + "_"
        + hashlib.md5(request.node.name.encode("utf-8")).hexdigest()[-4:]
    ).lstrip("_")
    if scylladb_cluster:
        print("USING KEYSPACE", keyspace_name)
        recreate_keyspace(scylladb_cluster, keyspace_name)
        session_mock = SessionMock(scylladb_cluster.connect(), keyspace=keyspace_name)
    else:
        session_mock = SessionMock(keyspace=keyspace_name)
    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.settings ( key TEXT, value TEXT, PRIMARY KEY(key));",
        [],
    )
    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.documents ( id bigint, doc blob, PRIMARY KEY(id));",
        [],
    )
    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.buckets "
        "( bucket bigint, hash bigint, doc_id bigint, PRIMARY KEY((bucket, hash), doc_id));",
        [],
    )
    return session_mock


@pytest.mark.asyncio
async def test_scylladb_store__initialize_cluster(monkeypatch, session_mock):
    monkeypatch.setattr(cassandra.cluster.Cluster, "__init__", lambda self: None)
    monkeypatch.setattr(cassandra.cluster.Cluster, "connect", lambda self: session_mock)

    storage = narrow_down.scylladb.ScyllaDBStore(
        cassandra.cluster.Cluster(), session_mock.test_keyspace
    )
    await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__initialize_session(session_mock):
    storage = narrow_down.scylladb.ScyllaDBStore(session_mock, session_mock.test_keyspace)
    await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_setting(session_mock):
    session_mock.add_mock_response("INSERT INTO <keyspace>.settings(key,value) VALUES (k,155);", [])
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.settings WHERE key=k;",
        [collections.namedtuple("Row", "value")("155")],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    assert await storage.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_scylladb_store__query_missing_setting(session_mock):
    session_mock.add_mock_response("SELECT value FROM <keyspace>.settings WHERE key=y;", [])
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    assert await storage.query_setting("y") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__uninitialized(session_mock):
    storage = narrow_down.scylladb.ScyllaDBStore(session_mock, session_mock.test_keyspace)
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__not_in(session_mock):
    session_mock.add_mock_response("SELECT value FROM <keyspace>.settings WHERE key=k;", [])
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__overwrite(session_mock):
    """Adding a duplicate before to see if that's also handled."""
    session_mock.add_mock_response("INSERT INTO <keyspace>.settings(key,value) VALUES (k,155);", [])
    session_mock.add_mock_response("INSERT INTO <keyspace>.settings(key,value) VALUES (k,268);", [])
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.settings WHERE key=k;",
        [collections.namedtuple("Row", "value")("268")],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    await storage.insert_setting(key="k", value="268")
    assert await storage.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__no_id(monkeypatch, session_mock):
    monkeypatch.setattr("random.randint", lambda **kwargs: 5)
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (5,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=True, id=None, doc=None)],
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.documents WHERE id=5;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__duplicate_doc(monkeypatch, session_mock):
    """Adding a duplicate before to see if that's also handled."""
    monkeypatch.setattr("random.randint", lambda **kwargs: 6)
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (6,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=True, id=None, doc=None)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    await storage.insert_document(document=b"abcd efgh")

    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (6,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=False, id=6, doc=b"abcd efgh")],
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.documents WHERE id=6;", [row(doc=b"abcd efgh")]
    )
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert id_out == 6
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id_duplicate(session_mock):
    """Adding a duplicate before to see if that's also handled."""
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__add_documents_to_bucket_and_query(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.buckets(bucket,hash,doc_id) VALUES (1,10,10);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.buckets(bucket,hash,doc_id) VALUES (1,20,20);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.buckets(bucket,hash,doc_id) VALUES (1,20,21);", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM to_bucket_and_query_e9fe.buckets WHERE bucket=1 AND hash=10;",
        [row(doc_id=10)],
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM to_bucket_and_query_e9fe.buckets WHERE bucket=1 AND hash=20;",
        [row(doc_id=20), row(doc_id=21)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await storage.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_scylladb_store__remove_document__given_id(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    session_mock.add_mock_response("DELETE FROM <keyspace>.documents WHERE id=1234;", [])
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"
    session_mock.add_mock_response("SELECT doc FROM <keyspace>.documents WHERE id=1234;", [])
    await storage.remove_document(id_out)
    with pytest.raises(KeyError):
        await storage.query_document(id_out)


@pytest.mark.asyncio
async def test_scylladb_store__remove_documents_to_bucket_and_query(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.buckets(bucket,hash,doc_id) VALUES (1,10,10);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.buckets(bucket,hash,doc_id) VALUES (1,10,20);", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.buckets WHERE bucket=1 AND hash=10;",
        [row(doc_id=10), row(doc_id=20)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]

    session_mock.add_mock_response(
        "DELETE FROM <keyspace>.buckets WHERE bucket=1 AND hash=10 AND doc_id=10;", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.buckets WHERE bucket=1 AND hash=10;", [row(doc_id=20)]
    )
    await storage.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]
