"""Type definitions of pure data classes and abstract types."""
import dataclasses
import enum
import pickle  # noqa
from dataclasses import dataclass
from typing import Any, Dict, NewType, Optional

import numpy as np
from numpy import typing as npt

from narrow_down.proto.stored_document_pb2 import StoredDocumentProto


class TooLowStorageLevel(Exception):
    """Raised if a feature is used for which a higher storage level is needed."""


class AlreadyInitialized(Exception):
    """Raised when initializing storage twice or changing immutable settings."""


class StorageLevel(enum.Flag):
    """Detail level of document persistence."""

    Minimal = enum.auto()
    """Minimal storage level. Only store the necessary data to perform the search."""
    Fingerprint = enum.auto()
    """In addition to Minimal, also store the fingerprint, e.g. the Minhashes"""
    Document = enum.auto()
    """Store the whole inserted document internally."""
    Full = Minimal | Fingerprint | Document
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
