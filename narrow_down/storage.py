"""Base classes and interfaces for storage."""
import asyncio
import dataclasses
import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, NewType, Optional

import numpy as np
from numpy import typing as npt

from narrow_down.proto.stored_document_pb2 import StoredDocumentProto

from ._rust import RustMemoryStore


class TooLowStorageLevel(Exception):  # noqa=N818
    """Raised if a feature is used for which a higher storage level is needed."""


class StorageLevel(enum.Flag):
    """Detail level of document persistence."""

    Minimal = enum.auto()
    """Minimal storage level. Only store the necessary data to perform the search."""
    Fingerprint = enum.auto()
    """In addition to Minimal, also store the fingerprint, e.g. the Minhashes"""
    Document = enum.auto()
    """Store the whole inserted document internally."""
    Full = Minimal | Fingerprint | Document  # pylint: disable=unsupported-binary-operation
    """Store everything."""


Fingerprint = NewType("Fingerprint", npt.NDArray[np.uint32])
"""Type representing the result of a minhashing operation"""


@dataclass(frozen=True)
class StoredDocument:
    """Data object combining all possible fields of a document stored."""

    id_: Optional[int] = None
    """Identifier used to distinguish the document from an identical one."""

    document: Optional[str] = None
    """The actual content to use for fuzzy matching, e.g. a full unprocessed sentence."""

    exact_part: Optional[str] = None
    """A string which should be matched exactly."""

    fingerprint: Optional[Fingerprint] = None
    """A fuzzy fingerprint of the document, e.g. a Minhash."""

    data: Optional[str] = None
    """Payload to persist together with the document in the internal data structures."""

    def serialize(self, storage_level: StorageLevel) -> bytes:
        """Serialize a document to bytes."""
        return StoredDocumentProto(
            fingerprint=list(self.fingerprint)
            if self.fingerprint is not None and storage_level & StorageLevel.Fingerprint
            else [],
            **{f: getattr(self, f) for f in _FIELDS_FOR_STORAGE_LEVEL[storage_level]},
        ).SerializeToString()

    @staticmethod
    def deserialize(doc: bytes, id_: int) -> "StoredDocument":
        """Deserialize a document from bytes."""
        p = StoredDocumentProto.FromString(doc)  # type: ignore
        args: Dict[str, Any] = dict(
            id_=id_,
        )
        if p.HasField("document"):
            args["document"] = p.document
        if p.HasField("exact_part"):
            args["exact_part"] = p.exact_part
        if p.fingerprint:
            args["fingerprint"] = Fingerprint(np.array(p.fingerprint, dtype=np.uint32))
        if p.HasField("data"):
            args["data"] = p.data
        return StoredDocument(**args)

    def without(self, *attributes: str) -> "StoredDocument":
        """Create a copy with the specified attributes left out.

        Args:
            attributes: The names of the attributes to leave empty

        Returns:
            A copy of the StoredDocument with all the attributes specified in attributes left out.
            So they will have their default value (None).
        """
        return StoredDocument(
            **{k: v for k, v in dataclasses.asdict(self).items() if k not in attributes}
        )


_FIELDS_FOR_STORAGE_LEVEL = {
    StorageLevel.Minimal: {"data"},
    StorageLevel.Document: {"data", "document", "exact_part"},
    StorageLevel.Fingerprint: {"data", "exact_part"},
    StorageLevel.Full: {"data", "document", "exact_part"},
}
"""Fields of StoredDocument which need to be serialized to reach a certain storage level."""


class StorageBackend(ABC):
    """Storage backend for a SimilarityStore."""

    async def initialize(
        self,
    ) -> "StorageBackend":
        """Initialize the database.

        Returns:
            self
        """
        return self

    @abstractmethod
    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        raise NotImplementedError

    @abstractmethod
    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key.

        Args:
            key: The identifier of the setting

        Returns:
            A string with the value. If the key does not exist or the storage is uninitialized
            None is returned.
        """
        raise NotImplementedError

    @abstractmethod
    async def insert_document(self, document: bytes, document_id: Optional[int] = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        raise NotImplementedError()

    @abstractmethod
    async def query_document(self, document_id: int) -> bytes:
        """Get the data belonging to a document.

        Args:
            document_id: Key under which the data is stored.

        Returns:
            The document value for the given ID.

        Raises:
            KeyError: If no document with the given ID is stored.
        """
        raise NotImplementedError

    async def query_documents(self, document_ids: List[int]) -> List[bytes]:
        """Get the data belonging to multiple documents.

        Args:
            document_ids: Key under which the data is stored.

        Returns:
            The list of document values for the given IDs.

        Raises:
            KeyError: If no document was found for at least one of the ids.
        """
        # Standard implementation of the base class. May be overloaded for specialization.
        return await asyncio.gather(*[self.query_document(doc_id) for doc_id in document_ids])

    @abstractmethod
    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        raise NotImplementedError()

    @abstractmethod
    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        raise NotImplementedError()

    @abstractmethod
    async def query_ids_from_bucket(self, bucket_id: int, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        raise NotImplementedError

    @abstractmethod
    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        raise NotImplementedError


class InMemoryStore(StorageBackend):
    """Rust implementation of InMemoryStore."""

    def __init__(self):
        """Create a new RustMemoryStore."""
        self.rms = RustMemoryStore()

    def serialize(self) -> bytes:
        """Serialize the data into a messagepack so that it can be persisted somewhere."""
        return self.rms.serialize()

    def to_file(self, file_path: str):
        """Serialize the data into a messagepack file with the given path."""
        return self.rms.to_file(file_path)

    @classmethod
    def deserialize(cls, msgpack: bytes) -> "InMemoryStore":
        """Deserialize an InMemoryStore object from messagepack."""
        obj = cls.__new__(cls)
        obj.rms = RustMemoryStore.deserialize(msgpack)
        return obj

    @classmethod
    def from_file(cls, file_path: str) -> "InMemoryStore":
        """Deserialize an InMemoryStore object the given messagepack file."""
        obj = cls.__new__(cls)
        obj.rms = RustMemoryStore.from_file(file_path)
        return obj

    async def insert_setting(self, key: str, value: str):
        """Store a setting as key-value pair."""
        self.rms.insert_setting(key, value)

    async def query_setting(self, key: str) -> Optional[str]:
        """Query a setting with the given key."""
        return self.rms.query_setting(key)

    async def insert_document(self, document: bytes, document_id: Optional[int] = None) -> int:
        """Add the data of a document to the storage and return its ID."""
        return self.rms.insert_document(document, document_id)

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
        doc = self.rms.query_document(document_id)
        if doc is None:
            raise KeyError(f"No document with id {document_id}")
        return doc

    async def remove_document(self, document_id: int):
        """Remove a document given by ID from the list of documents."""
        self.rms.remove_document(document_id)

    async def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Link a document to a bucket."""
        self.rms.add_document_to_bucket(bucket_id, document_hash, document_id)

    async def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]:
        """Get all document IDs stored in a bucket for a certain hash value."""
        return self.rms.query_ids_from_bucket(bucket_id, document_hash)

    async def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int):
        """Remove a document from a bucket."""
        self.rms.remove_id_from_bucket(bucket_id, document_hash, document_id)
