"""Storage backend based on SQLite."""
import sqlite3
from typing import Iterable, List, Optional

from narrow_down.storage import StorageBackend

QUERY_BATCH_SIZE = 500


class SQLiteStore(StorageBackend):
    """File-based storage backend for a SimilarityStore based on SQLite."""

    def __init__(self, db_filename: str, partitions: int = 128) -> None:
        """Create a new empty or connect to an existing SQLite database."""
        self.db_filename = db_filename
        self._connection = sqlite3.connect(self.db_filename, isolation_level="IMMEDIATE")
        # On reopening we can read the number of partitions from the db
        partitions_from_db = self._query_setting_sync("__sqlite_partitions")
        self.partitions = int(partitions_from_db) if partitions_from_db else partitions

    async def initialize(
        self,
    ) -> "SQLiteStore":
        """Initialize the tables in the SQLite database file.

        Returns:
            self
        """
        with self._connection as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS settings (key TEXT NOT NULL PRIMARY KEY, value TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS documents (id INTEGER NOT NULL PRIMARY KEY, doc BLOB)"
            )
            for i in range(self.partitions):
                conn.execute(
                    f"CREATE TABLE IF NOT EXISTS buckets_{i} ("
                    "bucket INTEGER NOT NULL, "
                    "hash INTEGER NOT NULL, "
                    "doc_id INTEGER NOT NULL"
                    ")"
                )
            conn.execute("PRAGMA synchronous = OFF")
            conn.execute("PRAGMA journal_mode = MEMORY")
            conn.commit()

        await self.insert_setting("__sqlite_partitions", str(self.partitions))

        return self

    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        with self._connection as conn:
            conn.execute(
                "INSERT INTO settings(key,value) VALUES (:key,:value) "
                "ON CONFLICT(key) DO UPDATE SET value=:value",
                dict(key=key, value=value),
            )

    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key.

        Args:
            key: The identifier of the setting

        Returns:
            A string with the value. If the key does not exist or the storage is uninitialized
            None is returned.

        Raises:
            sqlite3.OperationalError: In case the database query fails for any reason.
        """
        return self._query_setting_sync(key)

    def _query_setting_sync(self, key: str) -> Optional[str]:
        try:
            cursor = self._connection.execute("SELECT value FROM settings WHERE key=?", (key,))
            setting = cursor.fetchone()
            if setting is not None:
                return setting[0]
            return None
        except sqlite3.OperationalError as e:
            if "no such table: settings" in e.args:
                return None
            raise

    async def insert_document(self, document: bytes, document_id: int = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        with self._connection as conn:
            if document_id:
                conn.execute(
                    "INSERT INTO documents(id,doc) VALUES (:id,:doc) "
                    "ON CONFLICT(id) DO UPDATE SET doc=:doc",
                    dict(id=document_id, doc=document),
                )
                return document_id
            else:
                cursor = conn.execute(
                    "INSERT INTO documents(doc) VALUES (:doc) "
                    "ON CONFLICT(id) DO UPDATE SET doc=:doc",
                    dict(doc=document),
                )
                return cursor.lastrowid

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
        cursor = self._connection.execute("SELECT doc FROM documents WHERE id=?", (document_id,))
        doc = cursor.fetchone()
        if doc is None:
            raise KeyError(f"No document with id {document_id}")
        return doc[0]

    async def query_documents(self, document_ids: List[int]) -> List[bytes]:
        """Get the data belonging to multiple documents.

        Args:
            document_ids: Key under which the data is stored.

        Returns:
            The documents stored under the key `document_id` as bytes object.

        Raises:
            KeyError: If no document was found for at least one of the ids.
        """
        docs = {}
        for i in range(0, len(document_ids), QUERY_BATCH_SIZE):
            doc_id_batch = document_ids[i : i + QUERY_BATCH_SIZE]
            doc_ids_str = ",".join(map(str, map(int, doc_id_batch)))
            cursor = self._connection.execute(
                f"SELECT id, doc FROM documents WHERE id IN ({doc_ids_str})"
            )
            for id_, doc in cursor.fetchall():
                docs[id_] = doc
        return [docs[i] for i in document_ids]

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        with self._connection as conn:
            conn.execute("DELETE FROM documents WHERE id=?", (document_id,))

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        partition = int(document_hash % self.partitions)
        with self._connection as conn:
            conn.execute(
                f"INSERT INTO buckets_{partition}(bucket,hash,doc_id) VALUES (?,?,?)",  # noqa: S608
                (bucket_id, document_hash, document_id),
            )

    async def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        partition = int(document_hash % self.partitions)
        cursor = self._connection.execute(
            f"SELECT doc_id FROM buckets_{partition} WHERE bucket=? AND hash=?",  # noqa: S608
            (bucket_id, document_hash),
        )
        return [r[0] for r in cursor.fetchall()]

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        with self._connection as conn:
            partition = int(document_hash % self.partitions)
            conn.execute(
                f"DELETE FROM buckets_{partition} "  # noqa: S608
                "WHERE bucket=? AND hash=? AND doc_id=?",
                (bucket_id, document_hash, document_id),
            )
