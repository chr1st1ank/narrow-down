"""Base classes and interfaces for storage."""
import enum
from abc import ABC


class StorageMethod(enum.Flag):  # TODO: Review name
    """Detail level of document persistence."""

    Minimal = enum.auto()
    Fingerprint = enum.auto()
    Document = enum.auto()
    Full = Minimal | Fingerprint | Document


class StorageBackend(ABC):
    """Storage backend for a SimilarityStore."""

    # Init: storage_method: str = "lean", "document", "fingerprint"
    pass

    async def initialize(self) -> None:
        """Initialize the database."""
        pass


class InMemoryStore(StorageBackend):
    """In-Memory storage backend for a SimilarityStore."""

    def __init__(self) -> None:
        """Create a new empty store."""
        pass
