"""Base classes and interfaces for storage."""
from abc import ABC
from enum import Enum


class StorageMethod(Enum):  # TODO: Review name
    """Detail level of document persistence."""

    Minimal = 1
    Fingerprint = 2
    Document = 3
    Full = 4


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
