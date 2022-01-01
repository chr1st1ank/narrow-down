"""High-level API for indexing and retrieval of documents."""
from typing import Callable, List, Set

from narrow_down import hash, minhash
from narrow_down.data_types import StoredDocument
from narrow_down.storage import StorageBackend


class SimilarityStore:
    """Storage class for indexing and fuzzy search of documents."""

    def __init__(
        self,
        storage: StorageBackend,
        tokenize: Callable[[str], List[str]],
        hash_algorithm: hash.HashAlgorithm,
        max_false_negative_proba: float,
        max_false_positive_proba: float,
        similarity_threshold: float,
        # similarity_metric: str = "jaccard",  # Implement later
        # lsh_algorithm: str = "minhash",  # Implementlater
    ):
        """Create a new SimilarityStore object."""
        self._storage = storage
        self._tokenize = tokenize
        # if lsh_algorithm != "minhash":
        #     raise ValueError(f"Unknown algorithm {lsh_algorithm} in parameter lsh_algorithm!")
        self._minhash = minhash.MinHasher(hash_algorithm)
        # TODO: What about a setup with an existing database?
        lsh_config = minhash.LSH.find_optimal_config(
            max_false_negative_proba, max_false_positive_proba, similarity_threshold
        )
        self._lsh = minhash.LSH(**lsh_config)

    async def initialize(self):
        """Initialize the internal storage.

        Must be called for a new object. Should not be called when connecting to an existing
        database.
        """
        await self._storage.initialize()

    async def insert(
        self, document: str, *, document_id: str = None, exact_part: str = None, data: str = None
    ):
        """Index a new documents."""
        tokens = self._tokenize(document)
        fingerprint = self._minhash.minhash(tokens)
        await self._lsh.insert(
            fingerprint=fingerprint, document_id=document_id, exact_part=exact_part, data=data
        )

    async def query(self, document: str, *, exact_part=None) -> Set[StoredDocument]:
        """Query all similar documents."""
        tokens = self._tokenize(document)
        fingerprint = self._minhash.minhash(tokens)
        return await self._lsh.query(fingerprint=fingerprint, exact_part=exact_part)
