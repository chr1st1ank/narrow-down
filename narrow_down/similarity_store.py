"""High-level API for indexing and retrieval of documents."""
from typing import Callable, Collection

from narrow_down import _minhash, _tokenize
from narrow_down.data_types import StorageLevel, StoredDocument, TooLowStorageLevel
from narrow_down.storage import InMemoryStore, StorageBackend


class SimilarityStore:
    """Storage class for indexing and fuzzy search of documents."""

    def __init__(
        self,
        *,
        storage: StorageBackend = None,
        storage_level: StorageLevel = StorageLevel.Minimal,
        tokenize: Callable[[str], Collection[str]] = None,
        max_false_negative_proba: float = 0.05,
        max_false_positive_proba: float = 0.05,
        similarity_threshold: float = 0.75,
    ):
        """Create a new SimilarityStore object.

        Args:
            storage: Storage backend to use for persisting the data. Per default this is an
                in-memory backend.
            storage_level: The granularity of the internal storage mechanism. Per default nothing
                than the document IDs are stored.
            tokenize: The tokenization function to use to split the documents into smaller parts.
                E.g. the document may be split into words or into character n-grams. Per default
                word 3-grams are used.
            max_false_negative_proba: The target probability for false negatives. Setting this
                higher decreases the risk of not finding a similar document, but it leads to slower
                processing and more storage consumption.
            max_false_positive_proba: The target probability for false positives. Setting this
                higher decreases the risk of finding documents which are in reality not similar,
                but it leads to slower processing and more storage consumption.
            similarity_threshold: The minimum Jaccard similarity threshold used to identify two
                documents as being similar.
        """
        self._storage = storage or InMemoryStore()
        self._storage_level = storage_level
        self._tokenize = tokenize or (lambda s: _tokenize.word_ngrams(s, n=3))
        # TODO: What about a setup with an existing database?
        lsh_config = _minhash.find_optimal_config(
            jaccard_threshold=similarity_threshold,
            max_false_negative_proba=max_false_negative_proba,
            max_false_positive_proba=max_false_negative_proba,
        )
        self._minhash = _minhash.MinHasher(n_hashes=lsh_config.n_hashes)
        self._lsh = _minhash.LSH(lsh_config, storage=self._storage)

    async def initialize(self):
        """Initialize the internal storage.

        Must be called for a new object. Should not be called when connecting to an existing
        database.
        """
        await self._storage.initialize()

    async def insert(
        self, document: str, *, document_id: int = None, exact_part: str = None, data: str = None
    ) -> int:
        """Index a new document."""
        tokens = self._tokenize(document)
        fingerprint = self._minhash.minhash(tokens)
        stored_doc = StoredDocument(
            id_=document_id,
            document=document,
            exact_part=exact_part,
            fingerprint=fingerprint,
            data=data,
        )
        return await self._lsh.insert(document=stored_doc, storage_level=self._storage_level)

    async def remove_by_id(self, document_id: int, check_if_exists: bool = False) -> None:
        """Remove the document with the given ID from the internal data structures.

        Args:
            document_id: ID of the document to remove.
            check_if_exists: Raise a KeyError if the document does not exist.

        Raises:
            KeyError: If no document with the given ID is stored.
            TooLowStorageLevel: If the storage level is too low and fingerprints are not available.

        Notes:
            This method is only usable with StorageLevel 'Fingerprint' or higher.
        """
        if self._storage_level ^ StorageLevel.Fingerprint:
            raise TooLowStorageLevel(
                "Documents can only be removed with StorageLevel 'Fingerprint' or higher!"
            )
        await self._lsh.remove_by_id(document_id, check_if_exists)

    async def query(self, document: str, *, exact_part=None) -> Collection[StoredDocument]:
        """Query all similar documents."""
        tokens = self._tokenize(document)
        fingerprint = self._minhash.minhash(tokens)
        return await self._lsh.query(fingerprint=fingerprint, exact_part=exact_part)
