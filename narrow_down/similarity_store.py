"""High-level API for indexing and retrieval of documents."""
from typing import Callable, Iterable, List

from narrow_down import _minhash
from narrow_down.data_types import StoredDocument
from narrow_down.storage import StorageBackend


class SimilarityStore:
    """Storage class for indexing and fuzzy search of documents."""

    def __init__(
        self,
        /,
        storage: StorageBackend,
        tokenize: Callable[[str], List[str]],
        max_false_negative_proba: float,
        max_false_positive_proba: float,
        similarity_threshold: float,
    ):
        """Create a new SimilarityStore object.

        Args:
            storage: Storage backend to use for persisting the data. Per default this is an
                in-memory backend.
            tokenize: The tokenization function to use to split the documents into smaller parts.
                E.g. the document may be split into words or into character n-grams.
            max_false_negative_proba: The target probability for false negatives. Setting this
                higher decreases the risk of not finding a similar document, but it leads to slower
                processing and more storage consumption.
            max_false_positive_proba: The target probability for false positives. Setting this
                higher decreases the risk of finding documents which are in reality not similar,
                but it leads to slower processing and more storage consumption.
            similarity_threshold: The minimum Jaccard similarity threshold used to identify two
                documents as being similar.
        """
        self._storage = storage
        self._tokenize = tokenize
        # TODO: What about a setup with an existing database?
        lsh_config = _minhash.find_optimal_config(
            max_false_negative_proba, max_false_positive_proba, similarity_threshold
        )
        self._minhash = _minhash.MinHasher(n_hashes=lsh_config.n_hashes)
        self._lsh = _minhash.LSH(lsh_config, storage=storage)

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

    async def query(self, document: str, *, exact_part=None) -> Iterable[StoredDocument]:
        """Query all similar documents."""
        tokens = self._tokenize(document)
        fingerprint = self._minhash.minhash(tokens)
        return await self._lsh.query(fingerprint=fingerprint, exact_part=exact_part)
