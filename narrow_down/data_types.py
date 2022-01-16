"""Type definitions of pure data classes and abstract types."""
import dataclasses
import enum
import pickle  # noqa
from dataclasses import dataclass
from typing import NewType, Optional

import numpy as np
from numpy import typing as npt


class TooLowStorageLevel(Exception):
    """Raised if a feature is used for which a higher storage level is needed."""


class AlreadyInitialized(Exception):
    """Raised when initializing storage twice or changing immutable settings."""


class StorageLevel(enum.Flag):  # TODO: Review name
    """Detail level of document persistence."""

    Minimal = enum.auto()
    Fingerprint = enum.auto()
    Document = enum.auto()
    Full = Minimal | Fingerprint | Document


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

    # TODO: Pickle is far from optimal here.
    #   Maybe https://github.com/ultrajson/ultrajson is an alternative?
    def serialize(self, storage_level: StorageLevel) -> bytes:
        """Serialize a document to bytes."""
        return pickle.dumps(
            dataclasses.asdict(
                self,
                dict_factory=lambda items: {
                    k: v for k, v in items if k in _FIELDS_FOR_STORAGE_LEVEL[storage_level]
                },
            )
        )  # noqa

    @staticmethod
    def deserialize(doc: bytes, id_: int) -> "StoredDocument":
        """Deserialize a document from bytes."""
        d = pickle.loads(doc)  # noqa
        d["id_"] = id_
        return StoredDocument(**d)

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
    StorageLevel.Document: {"data", "document"},
    StorageLevel.Fingerprint: {"data", "exact_part", "fingerprint"},
    StorageLevel.Full: {"data", "document", "exact_part", "fingerprint"},
}
"""Fields of StoredDocument which need to be serialized to reach a certain storage level."""
