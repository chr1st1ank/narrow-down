"""Storage backend based on ScyllaDB.

ScyllaDB is a low-latency distributed key-value store, compatible with the Apache Cassandra
protocol. For details see _`https://www.scylladb.com/`.
"""
import asyncio
import contextlib
import random
import re
from typing import Dict, Iterable, List, Optional, Union

import cassandra.cluster  # type: ignore
import cassandra.query  # type: ignore

from narrow_down.storage import StorageBackend

QUERY_BATCH_SIZE = 50


def _wrap_future(f: cassandra.cluster.ResponseFuture):
    """Wrap a cassandra Future into an asyncio.Future object.

    Based on https://stackoverflow.com/questions/49350346/how-to-wrap-custom-future-to-use-with-asyncio-in-python.

    Args:
        f: future to wrap

    Returns:
        And asyncio.Future object which can be awaited.
    """  # noqa: E501
    loop = asyncio.get_event_loop()
    aio_future = loop.create_future()

    def on_result(result):
        loop.call_soon_threadsafe(aio_future.set_result, result)

    def on_error(exception, *_):
        loop.call_soon_threadsafe(aio_future.set_exception, exception)

    f.add_callback(on_result)
    f.add_errback(on_error)
    return aio_future


class ScyllaDBStore(StorageBackend):
    """Storage backend for a SimilarityStore using ScyllaDB."""

    def __init__(
        self,
        cluster_or_session: Union[cassandra.cluster.Cluster, cassandra.cluster.Session],
        keyspace: str,
        table_prefix: str = None,
    ) -> None:
        """Create a new empty or connect to an existing SQLite database.

        Args:
            cluster_or_session: Can be a cassandra cluster or a session object.
            keyspace: Name of the keyspace to use.
            table_prefix: A prefix to use for all table names in the database.

        Raises:
            ValueError: When the keyspace name is invalid.
        """
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", keyspace):
            raise ValueError(f"Invalid keyspace name: {keyspace}")
        if table_prefix and not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_prefix):
            raise ValueError(f"Invalid table_prefix: {table_prefix}")
        if isinstance(cluster_or_session, cassandra.cluster.Cluster):
            self._scylla_cluster = cluster_or_session
            self._scylla_session = None
        else:
            self._scylla_cluster = None
            self._scylla_session = cluster_or_session
        self._keyspace = keyspace
        self._table_prefix = table_prefix or ""
        self._prepared_statements: Dict[str, cassandra.query.PreparedStatement] = {}

    @contextlib.contextmanager
    def _session(self) -> cassandra.cluster.Session:
        """Get or create a cassandra session."""
        if (not self._scylla_session) and self._scylla_cluster:
            self._scylla_session = self._scylla_cluster.connect()
        yield self._scylla_session

    async def _execute(self, session, query, parameters=None, timeout=None):
        """Execute a cassandra query with asyncio."""
        return await _wrap_future(
            session.execute_async(
                query=query, parameters=parameters, timeout=timeout or cassandra.cluster._NOT_SET
            )
        )

    async def initialize(
        self,
    ) -> "ScyllaDBStore":
        """Initialize the tables in the SQLite database file.

        Returns:
            self
        """
        # Note: CQL does not know unsigned integers.
        #  So we need to take the 64bit (signed) bigint to hold a 32bit unsigned int safely.

        create_settings = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.{self._table_prefix}settings ("
            "   key TEXT, "
            "   value TEXT, "
            "   PRIMARY KEY(key)"
            ");",
            is_idempotent=True,
        )
        create_documents = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.{self._table_prefix}documents ("
            "   id bigint, "
            "   doc blob, "
            "   PRIMARY KEY(id)"
            ");",
            is_idempotent=True,
        )
        create_buckets = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.{self._table_prefix}buckets ("
            "   bucket bigint, "
            "   hash bigint, "
            "   doc_id bigint, "
            "   PRIMARY KEY((bucket, hash), doc_id)"
            ");",
            is_idempotent=True,
        )
        with self._session() as session:
            await self._execute(session, create_settings, timeout=30)
            await self._execute(session, create_documents, timeout=30)
            await self._execute(session, create_buckets, timeout=30)
            self._prepared_statements["set_setting"] = session.prepare(
                f"INSERT INTO {self._keyspace}.{self._table_prefix}"
                "settings(key,value) VALUES (?,?);"
            )
            self._prepared_statements["get_setting"] = session.prepare(
                f"SELECT value FROM {self._keyspace}.{self._table_prefix}settings WHERE key=?;"
            )
            self._prepared_statements["set_doc"] = session.prepare(
                f"INSERT INTO {self._keyspace}.{self._table_prefix}documents(id,doc) VALUES (?,?);"
            )
            self._prepared_statements["set_doc_checked"] = session.prepare(
                f"INSERT INTO {self._keyspace}.{self._table_prefix}"
                "documents(id,doc) VALUES (?,?) IF NOT EXISTS;"
            )
            self._prepared_statements["get_doc"] = session.prepare(
                f"SELECT doc FROM {self._keyspace}.{self._table_prefix}documents WHERE id=?;"
            )
            self._prepared_statements["del_doc"] = session.prepare(
                f"DELETE FROM {self._keyspace}.{self._table_prefix}documents WHERE id=?;"
            )
            self._prepared_statements["add_doc_to_bucket"] = session.prepare(
                f"INSERT INTO {self._keyspace}.{self._table_prefix}"
                "buckets(bucket,hash,doc_id) VALUES (?,?,?);"
            )
            self._prepared_statements["get_docs_from_bucket"] = session.prepare(
                f"SELECT doc_id FROM {self._keyspace}.{self._table_prefix}"
                "buckets WHERE bucket=? AND hash=?;"
            )
            self._prepared_statements["del_doc_from_bucket"] = session.prepare(
                f"DELETE FROM {self._keyspace}.{self._table_prefix}"
                "buckets WHERE bucket=? AND hash=? AND doc_id=?;"
            )
        for statement in self._prepared_statements.values():
            statement.is_idempotent = True

        return self

    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        with self._session() as session:
            await self._execute(session, self._prepared_statements["set_setting"], (key, value))

    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key.

        Args:
            key: The identifier of the setting

        Returns:
            A string with the value. If the key does not exist or the storage is uninitialized
            None is returned.

        Raises:
            cassandra.DriverException: In case the database query fails for any reason.
        """  # noqa: DAR401
        with self._session() as session:
            try:
                result_list = await self._execute(
                    session, self._prepared_statements["get_setting"], (key,)
                )
                return None if not result_list else result_list[0].value
            except KeyError as e:
                if "get_setting" in e.args:
                    return None
                raise  # Don't swallow unknown errors

    async def insert_document(self, document: bytes, document_id: int = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        with self._session() as session:
            if document_id:
                await self._execute(
                    session,
                    self._prepared_statements["set_doc"],
                    (document_id, document),
                )
                return document_id
            else:
                for _ in range(10):
                    doc_id = random.randint(a=0, b=2**32)
                    result = await self._execute(
                        session,
                        self._prepared_statements["set_doc_checked"],
                        (doc_id, document),
                    )
                    inserted_successfully = result[0].applied
                    if (
                        inserted_successfully
                        or result[0].id == doc_id
                        and result[0].doc == document
                    ):
                        return doc_id
                raise RuntimeError("Unable to find an ID for a document. This should never happen.")

    async def query_document(self, document_id: int) -> bytes:
        """Get the data belonging to a document.

        Args:
            document_id: The id of the document. This ID is created and returned by the
                `insert_document` method.

        Returns:
            The document stored under the key `document_id` as bytes object.

        Raises:
            KeyError: If the document is not stored.
        """
        with self._session() as session:
            docs = await self._execute(
                session, self._prepared_statements["get_doc"], (document_id,)
            )
        if not docs:
            raise KeyError(f"No document with id {document_id}")
        return docs[0].doc

    async def query_documents(self, document_ids: List[int]) -> List[bytes]:
        """Get the data belonging to multiple documents.

        Args:
            document_ids: Key under which the data is stored.

        Returns:
            The documents stored under the key `document_id` as bytes object.

        Raises:
            KeyError: If no document was found for at least one of the ids.
        """
        if len(document_ids) > QUERY_BATCH_SIZE:
            with self._session() as session:
                result_doc_dicts = await asyncio.gather(
                    *[
                        self._query_document_batch(session, document_ids[i : i + QUERY_BATCH_SIZE])
                        for i in range(0, len(document_ids), QUERY_BATCH_SIZE)
                    ]
                )
                doc_dicts = {id_: doc for d in result_doc_dicts for id_, doc in d.items()}
                return [doc_dicts[i] for i in document_ids]
        else:
            docs: List[bytes] = await asyncio.gather(
                *[self.query_document(id_) for id_ in document_ids]
            )
            return docs

    async def _query_document_batch(self, session, doc_id_batch):
        doc_ids_str = ",".join(map(str, map(int, doc_id_batch)))
        query = (
            f"select id, doc from {self._keyspace}.{self._table_prefix}documents "
            f"where id IN ({doc_ids_str});"
        )
        result_docs = {r.id: r.doc for r in await self._execute(session, query)}
        return result_docs

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        with self._session() as session:
            await self._execute(session, self._prepared_statements["del_doc"], (document_id,))

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        with self._session() as session:
            await self._execute(
                session,
                self._prepared_statements["add_doc_to_bucket"],
                (bucket_id, document_hash, document_id),
            )

    async def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        with self._session() as session:
            rows = await self._execute(
                session,
                self._prepared_statements["get_docs_from_bucket"],
                (bucket_id, document_hash),
            )
        return [r.doc_id for r in rows]

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        with self._session() as session:
            await self._execute(
                session,
                self._prepared_statements["del_doc_from_bucket"],
                (bucket_id, document_hash, document_id),
            )
