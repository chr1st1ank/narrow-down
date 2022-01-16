"""Base classes and interfaces for storage."""
from abc import ABC
from collections import defaultdict
from typing import Dict, Iterable, Optional, Set

from . import hash


class StorageBackend(ABC):
    """Storage backend for a SimilarityStore."""

    async def initialize(
        self,
    ) -> "StorageBackend":
        """Initialize the database.

        Returns:
            self

        Implementations may raise an error if the backend is already initialized.
        """
        return self

    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        raise NotImplementedError

    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key.

        Args:
            key: The identifier of the setting

        Returns:
            A string with the value. If the key does not exist or the storage is uninitialized
            None is returned.
        """  # noqa: DAR202,DAR401
        raise NotImplementedError

    async def insert_document(self, document: bytes, document_id: int = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        raise NotImplementedError()

    async def query_document(self, document_id: int) -> bytes:
        """Get the data belonging to a document.

        Args:
            document_id: Key under which the data is stored.

        Raises:
            KeyError: If no document with the given ID is stored.
        """  # noqa: DAR401
        raise NotImplementedError

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        raise NotImplementedError()

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        raise NotImplementedError()

    async def query_ids_from_bucket(self, bucket_id: int, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        raise NotImplementedError

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        raise NotImplementedError


class InMemoryStore(StorageBackend):
    """In-Memory storage backend for a SimilarityStore."""

    def __init__(self) -> None:
        """Create a new empty in memory database."""
        self._settings: Dict[str, str] = {}
        self._documents: Dict[int, bytes] = {}
        self._buckets: Dict[int, Dict[int, Set[int]]] = defaultdict(lambda: defaultdict(set))

    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        self._settings[key] = value

    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key."""
        return self._settings.get(key)

    async def insert_document(self, document: bytes, document_id: int = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        if document_id:
            index = document_id
        else:
            index = self._find_next_document_id(document)
        self._documents[index] = document
        return index

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
        return self._documents[document_id]

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        del self._documents[document_id]

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        self._buckets[bucket_id][document_hash].add(document_id)

    async def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        return self._buckets[bucket_id][document_hash]

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        self._buckets[bucket_id][document_hash].remove(document_id)

    def _find_next_document_id(self, document: bytes) -> int:
        """Find an unused document ID."""
        x: int = hash.xxhash_32bit(document)
        while x in self._documents:
            x += 1
        return x
