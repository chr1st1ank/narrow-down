"""Tests for the `narrow_down.scylladb` module."""
import collections
import hashlib
import os
import re
from typing import Dict, List, NamedTuple, Tuple, Union

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

    def __init__(self, real_session=None, keyspace="", table_prefix=None):
        """Create a new Session object."""
        self.test_keyspace = keyspace
        self.table_prefix = table_prefix or ""
        self._real_session: cassandra.cluster.Session = real_session
        self._query_responses: Dict[str, Union[List[NamedTuple], Exception]] = {}
        self._shutdown = False

    def add_mock_response(self, request: str, response: Union[List[NamedTuple], Exception]):
        """Add an expected query with response list."""
        query = request.replace("<keyspace>", self.test_keyspace)
        query = query.replace("<table_prefix>", self.table_prefix)
        self._query_responses[query] = response

    def del_mock_response(self, request: str):
        """Remove one of the stored expected queries."""
        query = request.replace("<keyspace>", self.test_keyspace)
        query = query.replace("<table_prefix>", self.table_prefix)
        del self._query_responses[query]

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
            if not isinstance(self._query_responses[query_string], Exception):
                assert response.all() == self._query_responses[query_string]
        return SessionMock._Result(self._query_responses[query_string])

    def execute_async(self, query, parameters, timeout=0.1):
        """Call session.execute() to run a query asynchronously."""
        assert not self._shutdown
        query_string = self._prepare_query_string(query, parameters)

        if self._real_session:
            future = self._real_session.execute_async(query, parameters, timeout)
            if not isinstance(self._query_responses[query_string], Exception):
                assert future.result().all() == self._query_responses.get(query_string)
            return future

        class FakeFuture:
            @staticmethod
            def add_callback(f):
                if not isinstance(self._query_responses[query_string], Exception):
                    f(self._query_responses[query_string])

            @staticmethod
            def add_errback(f):
                if isinstance(self._query_responses[query_string], Exception):
                    f(self._query_responses[query_string])

        return FakeFuture

    def _prepare_query_string(self, statement, parameters: Tuple):
        prepared = (
            re.sub(r"\s+", " ", statement if isinstance(statement, str) else statement.query_string)
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


@pytest.fixture(scope="function", params=[None, "abc_d_"])
def table_prefix(request):
    return request.param


@pytest.fixture(scope="function")
def session_mock(request, scylladb_cluster, table_prefix):
    keyspace_name = (
        request.node.name[-20 : request.node.name.find("[")]
        + "_"
        + hashlib.md5(request.node.name.encode("utf-8")).hexdigest()[-4:]
    ).lstrip("_")
    if scylladb_cluster:
        print("USING KEYSPACE", keyspace_name)
        recreate_keyspace(scylladb_cluster, keyspace_name)
        session_mock = SessionMock(
            scylladb_cluster.connect(), keyspace=keyspace_name, table_prefix=table_prefix
        )
    else:
        session_mock = SessionMock(keyspace=keyspace_name, table_prefix=table_prefix)

    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.<table_prefix>"
        "settings ( key TEXT, value TEXT, PRIMARY KEY(key));",
        [],
    )
    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.<table_prefix>"
        "documents ( id bigint, doc blob, PRIMARY KEY(id));",
        [],
    )
    session_mock.add_mock_response(
        "CREATE TABLE IF NOT EXISTS <keyspace>.<table_prefix>buckets "
        "( bucket bigint, hash bigint, doc_id bigint, PRIMARY KEY((bucket, hash), doc_id));",
        [],
    )
    return session_mock


@pytest.mark.asyncio
async def test_scylladb_store__initialize_cluster(monkeypatch, session_mock):
    monkeypatch.setattr(cassandra.cluster.Cluster, "__init__", lambda self: None)
    monkeypatch.setattr(cassandra.cluster.Cluster, "connect", lambda self: session_mock)
    storage = narrow_down.scylladb.ScyllaDBStore(
        cassandra.cluster.Cluster(), session_mock.test_keyspace, session_mock.table_prefix
    )
    await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__initialize_session(session_mock):
    storage = narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    )
    await storage.initialize()


@pytest.mark.asyncio
async def test_scylladb_store__check_keyspace():
    with pytest.raises(ValueError):
        narrow_down.scylladb.ScyllaDBStore(None, "; DROP KEYSPACE x;")


@pytest.mark.asyncio
async def test_scylladb_store__check_table_prefix():
    with pytest.raises(ValueError):
        narrow_down.scylladb.ScyllaDBStore(None, "keyspace", "; DROP KEYSPACE x;")


@pytest.mark.asyncio
async def test_scylladb_store__handle_query_error(monkeypatch, session_mock):
    from cassandra.cluster import OperationTimedOut

    def raise_error(future: cassandra.cluster.ResponseFuture):
        future._set_final_exception(OperationTimedOut("Timeout for testing"))

    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>settings(key,value) VALUES (k,155);",
        OperationTimedOut("Timeout for testing"),
    )
    monkeypatch.setattr("cassandra.cluster.ResponseFuture.send_request", raise_error)

    with pytest.raises(OperationTimedOut):
        await storage.insert_setting(key="k", value="155")


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_setting(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>settings(key,value) VALUES (k,155);", []
    )
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.<table_prefix>settings WHERE key=k;",
        [collections.namedtuple("Row", "value")("155")],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    assert await storage.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_scylladb_store__query_missing_setting(session_mock):
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.<table_prefix>settings WHERE key=y;", []
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    assert await storage.query_setting("y") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__uninitialized(session_mock):
    storage = narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    )
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__query_setting__not_in(session_mock):
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.<table_prefix>settings WHERE key=k;", []
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    assert await storage.query_setting("k") is None


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__overwrite(session_mock):
    """Adding a duplicate before to see if that's also handled."""
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>settings(key,value) VALUES (k,155);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>settings(key,value) VALUES (k,268);", []
    )
    session_mock.add_mock_response(
        "SELECT value FROM <keyspace>.<table_prefix>settings WHERE key=k;",
        [collections.namedtuple("Row", "value")("268")],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    await storage.insert_setting(key="k", value="155")
    await storage.insert_setting(key="k", value="268")
    assert await storage.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__no_id(monkeypatch, session_mock):
    monkeypatch.setattr("random.randint", lambda **kwargs: 5)
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>"
        "documents(id,doc) VALUES (5,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=True, id=None, doc=None)],
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=5;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__no_id_found(monkeypatch, session_mock):
    """Check if the driver tries a couple of times before giving up finding a random ID."""
    n_attempts = 0

    async def return_failure(*args, **kwargs):
        nonlocal n_attempts
        n_attempts += 1
        return [row(applied=False, id=4, doc=b"abcd efgh")]

    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()

    monkeypatch.setattr("random.randint", lambda **kwargs: 5)
    monkeypatch.setattr(storage, "_execute", return_failure)
    with pytest.raises(RuntimeError):
        await storage.insert_document(document=b"abcd efgh")
    assert n_attempts == 10


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__duplicate_doc(monkeypatch, session_mock):
    """Adding a duplicate before to see if that's also handled."""
    monkeypatch.setattr("random.randint", lambda **kwargs: 6)
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>"
        "documents(id,doc) VALUES (6,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=True, id=None, doc=None)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    await storage.insert_document(document=b"abcd efgh")

    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>"
        "documents(id,doc) VALUES (6,b'abcd efgh') IF NOT EXISTS;",
        [row(applied=False, id=6, doc=b"abcd efgh")],
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=6;", [row(doc=b"abcd efgh")]
    )
    id_out = await storage.insert_document(document=b"abcd efgh")
    assert id_out == 6
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__insert_query_document__given_id_duplicate(session_mock):
    """Adding a duplicate before to see if that's also handled."""
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_scylladb_store__query_documents(session_mock):
    """Testing mass querying of documents."""
    doc_ids = list(range(100, 180, 1))
    doc_vals = [f"abcd efgh ijkl mnop qrst {doc_id}".encode("utf-8") for doc_id in doc_ids]

    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    for doc_id, doc_val in zip(doc_ids, doc_vals):
        session_mock.add_mock_response(
            "INSERT INTO <keyspace>.<table_prefix>documents(id,doc) "
            f"VALUES ({doc_id},{doc_val});",
            [],
        )
        id_out = await storage.insert_document(document=doc_val, document_id=doc_id)
        assert id_out == doc_id
    session_mock.add_mock_response(
        f"select id, doc from <keyspace>.<table_prefix>documents where id IN "
        f"({','.join(map(str,doc_ids[:50]))});",
        [row(id=i, doc=doc_val) for i, doc_val in zip(doc_ids[:50], doc_vals[:50])],
    )
    session_mock.add_mock_response(
        f"select id, doc from <keyspace>.<table_prefix>documents where id IN "
        f"({','.join(map(str,doc_ids[50:100]))});",
        [row(id=i, doc=doc_val) for i, doc_val in zip(doc_ids[50:100], doc_vals[50:100])],
    )

    assert await storage.query_documents(doc_ids) == doc_vals


@pytest.mark.asyncio
async def test_scylladb_store__add_documents_to_bucket_and_query(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>buckets(bucket,hash,doc_id) VALUES (1,10,10);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>buckets(bucket,hash,doc_id) VALUES (1,20,20);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>buckets(bucket,hash,doc_id) VALUES (1,20,21);", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.<table_prefix>buckets WHERE bucket=1 AND hash=10;",
        [row(doc_id=10)],
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.<table_prefix>buckets WHERE bucket=1 AND hash=20;",
        [row(doc_id=20), row(doc_id=21)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await storage.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_scylladb_store__remove_document__given_id(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>documents(id,doc) VALUES (1234,b'abcd efgh');", []
    )
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=1234;", [row(doc=b"abcd efgh")]
    )
    session_mock.add_mock_response(
        "DELETE FROM <keyspace>.<table_prefix>documents WHERE id=1234;", []
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    id_out = await storage.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await storage.query_document(id_out) == b"abcd efgh"
    session_mock.add_mock_response(
        "SELECT doc FROM <keyspace>.<table_prefix>documents WHERE id=1234;", []
    )
    await storage.remove_document(id_out)
    with pytest.raises(KeyError):
        await storage.query_document(id_out)


@pytest.mark.asyncio
async def test_scylladb_store__remove_documents_to_bucket_and_query(session_mock):
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>buckets(bucket,hash,doc_id) VALUES (1,10,10);", []
    )
    session_mock.add_mock_response(
        "INSERT INTO <keyspace>.<table_prefix>buckets(bucket,hash,doc_id) VALUES (1,10,20);", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.<table_prefix>buckets WHERE bucket=1 AND hash=10;",
        [row(doc_id=10), row(doc_id=20)],
    )
    storage = await narrow_down.scylladb.ScyllaDBStore(
        session_mock, session_mock.test_keyspace, session_mock.table_prefix
    ).initialize()
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await storage.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=20)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10, 20]

    session_mock.add_mock_response(
        "DELETE FROM <keyspace>.<table_prefix>buckets WHERE bucket=1 AND hash=10 AND doc_id=10;", []
    )
    session_mock.add_mock_response(
        "SELECT doc_id FROM <keyspace>.<table_prefix>buckets WHERE bucket=1 AND hash=10;",
        [row(doc_id=20)],
    )
    await storage.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await storage.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [20]
