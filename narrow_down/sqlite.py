"""Storage backend based on SQLite."""
import sqlite3
from typing import Iterable, Optional

from narrow_down.data_types import AlreadyInitialized
from narrow_down.storage import StorageBackend


class SQLiteStore(StorageBackend):
    """File-based storage backend for a SimilarityStore based on SQLite."""

    def __init__(self, db_filename: str) -> None:
        """Create a new empty or connect to an existing SQLite database."""
        self.db_filename = db_filename
        self._connection = sqlite3.connect(self.db_filename, isolation_level="IMMEDIATE")

    async def initialize(
        self,
    ) -> "SQLiteStore":
        """Initialize the tables in the SQLite database file.

        Returns:
            self

        Raises:
            AlreadyInitialized: If the database file is already initialized
        """
        try:
            with self._connection as conn:
                conn.execute("CREATE TABLE settings (key TEXT NOT NULL PRIMARY KEY, value TEXT)")
                conn.execute("CREATE TABLE documents (id INTEGER NOT NULL PRIMARY KEY, doc BLOB)")
                conn.execute(
                    "CREATE TABLE buckets ("
                    "bucket INTEGER NOT NULL, "
                    "hash INTEGER NOT NULL, "
                    "doc_id INTEGER NOT NULL"
                    ")"
                )
        except sqlite3.OperationalError as e:
            raise AlreadyInitialized from e

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

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        with self._connection as conn:
            conn.execute("DELETE FROM documents WHERE id=?", (document_id,))

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        with self._connection as conn:
            conn.execute(
                "INSERT INTO buckets(bucket,hash,doc_id) VALUES (?,?,?)",
                (bucket_id, document_hash, document_id),
            )

    async def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        cursor = self._connection.execute(
            "SELECT doc_id FROM buckets WHERE bucket=? AND hash=?", (bucket_id, document_hash)
        )
        return [r[0] for r in cursor.fetchall()]

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        with self._connection as conn:
            conn.execute(
                "DELETE FROM buckets WHERE bucket=? AND hash=? AND doc_id=?",
                (bucket_id, document_hash, document_id),
            )
