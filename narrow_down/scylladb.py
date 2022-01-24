"""Storage backend based on ScyllaDB.

ScyllaDB is a low-latency distributed key-value store, compatible with the Apache Cassandra
protocol. For details see _`https://www.scylladb.com/`.
"""
import asyncio
import contextlib
import random
import re
from typing import Dict, Iterable, Optional, Union

import cassandra.cluster  # type: ignore
import cassandra.query  # type: ignore

from narrow_down.storage import StorageBackend


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
    ) -> None:
        """Create a new empty or connect to an existing SQLite database.

        TODO: Describe cluster/session

        Args:
            cluster_or_session: Can be a cassandra cluster or a session object.
            keyspace: Name of the keyspace to use.

        Raises:
            ValueError: When the keyspace name is invalid.
        """
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", keyspace):
            raise ValueError(f"Invalid keyspace name: {keyspace}")
        self._cluster_or_session = cluster_or_session
        self._keyspace = keyspace
        self._prepared_statements: Dict[str, cassandra.query.PreparedStatement] = {}

    @contextlib.contextmanager
    def _session(self) -> cassandra.cluster.Session:
        """Get or create a cassandra session."""
        if isinstance(self._cluster_or_session, cassandra.cluster.Cluster):
            with self._cluster_or_session.connect() as session:
                yield session
        else:
            yield self._cluster_or_session

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

        Raises:
            AlreadyInitialized: If the database file is already initialized
        """
        # Note: CQL does not know unsigned integers.
        #  So we need to take the 64bit (signed) bigint to hold a 32bit unsigned int safely.

        create_settings = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.settings ("
            "   key TEXT, "
            "   value TEXT, "
            "   PRIMARY KEY(key)"
            ");",
            is_idempotent=True,
        )
        create_documents = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.documents ("
            "   id bigint, "
            "   doc blob, "
            "   PRIMARY KEY(id)"
            ");",
            is_idempotent=True,
        )
        create_buckets = cassandra.query.SimpleStatement(
            f"CREATE TABLE IF NOT EXISTS {self._keyspace}.buckets ("
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
                f"INSERT INTO {self._keyspace}.settings(key,value) VALUES (?,?);"
            )
            self._prepared_statements["get_setting"] = session.prepare(
                f"SELECT value FROM {self._keyspace}.settings WHERE key=?;"
            )
            self._prepared_statements["set_doc"] = session.prepare(
                f"INSERT INTO {self._keyspace}.documents(id,doc) VALUES (?,?);"
            )
            self._prepared_statements["set_doc_checked"] = session.prepare(
                f"INSERT INTO {self._keyspace}.documents(id,doc) VALUES (?,?) IF NOT EXISTS;"
            )
            self._prepared_statements["get_doc"] = session.prepare(
                f"SELECT doc FROM {self._keyspace}.documents WHERE id=?;"
            )
            self._prepared_statements["del_doc"] = session.prepare(
                f"DELETE FROM {self._keyspace}.documents WHERE id=?;"
            )
            self._prepared_statements["add_doc_to_bucket"] = session.prepare(
                f"INSERT INTO {self._keyspace}.buckets(bucket,hash,doc_id) VALUES (?,?,?);"
            )
            self._prepared_statements["get_docs_from_bucket"] = session.prepare(
                f"SELECT doc_id FROM {self._keyspace}.buckets WHERE bucket=? AND hash=?;"
            )
            self._prepared_statements["del_doc_from_bucket"] = session.prepare(
                f"DELETE FROM {self._keyspace}.buckets WHERE bucket=? AND hash=? AND doc_id=?;"
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
                    doc_id = random.randint(a=0, b=2 ** 32)
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
