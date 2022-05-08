"""High-level API for indexing and retrieval of documents."""
import re
import warnings
from typing import Callable, Collection, Iterable, List, Union

from narrow_down import _minhash, _tokenize
from narrow_down._minhash import MinhashLshConfig
from narrow_down.storage import (
    InMemoryStore,
    StorageBackend,
    StorageLevel,
    StoredDocument,
    TooLowStorageLevel,
)


class SimilarityStore:
    """Storage class for indexing and fuzzy search of documents."""

    __slots__ = (
        "_minhasher",
        "_similarity_threshold",
        "_lsh",
        "_storage",
        "_storage_level",
        "_tokenize",
        "_tokenize_callable",
        "_lsh_config",
    )

    def __init__(self):  # noqa: D107  # Not meant to be called, therefore omitting docstring.
        warnings.warn(
            "The __init__ function is not meant to be called in isolation. "
            "To create a SimilarityStore object use the coroutine functions "
            "SimilarityStore.create() or SimilarityStore.load_from_storage()."
        )
        self._minhasher: _minhash.MinHasher
        self._similarity_threshold: float
        self._lsh: _minhash.LSH
        self._storage: StorageBackend
        self._storage_level: StorageLevel
        self._tokenize: Union[str, Callable[[str], Collection[str]]]
        self._tokenize_callable: Callable[[str], Collection[str]]
        self._lsh_config: MinhashLshConfig

    @classmethod
    async def create(
        cls,
        *,
        storage: StorageBackend = None,
        storage_level: StorageLevel = StorageLevel.Minimal,
        tokenize: Union[str, Callable[[str], Collection[str]]] = None,
        max_false_negative_proba: float = 0.05,
        max_false_positive_proba: float = 0.05,
        similarity_threshold: float = 0.75,
    ) -> "SimilarityStore":
        """Create a new SimilarityStore object.

        Args:
            storage: Storage backend to use for persisting the data. Per default this is an
                in-memory backend.
            storage_level: The granularity of the internal storage mechanism. Per default nothing
                than the document IDs are stored.
            tokenize: The tokenization function to use to split the documents into smaller parts.
                E.g. the document may be split into words or into character n-grams. Per default
                word 3-grams are used.

                Built-in tokenizers can be used by passing their name and parameters as string.
                Options:

                - ``"word_ngrams(n)"`` enables the word-ngram tokenizer
                  :func:`narrow_down._tokenize.word_ngrams`
                - ``"char_ngrams(n)"`` or ``"char_ngrams(n,c)"`` enables the character-ngram
                  tokenizer :func:`narrow_down._tokenize.char_ngrams`.

                It is also possible to pass a custom function (not as string in this case, but
                the function itself). In this case it needs to be taken care to specify the same
                function again when saving and re-creating the SimilarityStore object.
            max_false_negative_proba: The target probability for false negatives. Setting this
                higher decreases the risk of not finding a similar document, but it leads to slower
                processing and more storage consumption.
            max_false_positive_proba: The target probability for false positives. Setting this
                higher decreases the risk of finding documents which are in reality not similar,
                but it leads to slower processing and more storage consumption.
            similarity_threshold: The minimum Jaccard similarity threshold used to identify two
                documents as being similar.

        Raises:
            ValueError: If the function specified with ``tokenize`` cannot be found.

        Returns:
            A new SimilarityStore object with already initialized storage.

        ..
          # noqa: DAR101 max_false_negative_proba
          # noqa: DAR101 max_false_positive_proba
          # noqa: DAR101 similarity_threshold
        """
        obj = await cls._create_object_base(storage, storage_level, similarity_threshold, tokenize)
        obj._lsh_config = _minhash.find_optimal_config(
            jaccard_threshold=similarity_threshold,
            max_false_negative_proba=max_false_negative_proba,
            max_false_positive_proba=max_false_positive_proba,
        )
        await obj._initialize_storage()
        return obj

    @classmethod
    async def load_from_storage(
        cls, storage: StorageBackend, tokenize: Union[str, Callable[[str], Collection[str]]] = None
    ) -> "SimilarityStore":
        """Load a SimilarityStore object from already initialized storage.

        Args:
            storage: A StorageBackend object which must already have been initialized by a
                SimilarityStore object before.
            tokenize: The tokenization function originally specified in the init when initializing
                the Similarity Store. See :func:`narrow_down.SimilarityStore.__init__`.

        Returns:
            A SimilarityStore object using the given storage backend and with the settings stored
            in the storage.

        Raises:
            TypeError: If settings in the storage are missing, corrupt or cannot be deserialized.
            ValueError: If the function specified with ``tokenize`` cannot be found.
        """
        storage_level = StorageLevel(
            # Let it throw TypeError if None:
            int(await storage.query_setting("storage_level"))  # type: ignore
        )
        similarity_threshold = float(
            # Let it throw TypeError if None:
            await storage.query_setting("similarity_threshold")  # type: ignore
        )
        tokenize_spec: Union[
            str, Callable[[str], Collection[str]], None
        ] = await storage.query_setting("tokenize")
        if tokenize_spec == "custom":
            tokenize_spec = tokenize
        if not tokenize_spec:
            raise TypeError("tokenize function cannot be deserialized")
        lsh_config_setting = await storage.query_setting("lsh_config")
        if not lsh_config_setting:
            raise TypeError("lsh_config setting could not be read from storage.")
        lsh_config = MinhashLshConfig.from_json(lsh_config_setting)

        simstore = await cls._create_object_base(
            storage=storage,
            storage_level=storage_level,
            similarity_threshold=similarity_threshold,
            tokenize=tokenize_spec,
        )
        simstore._lsh_config = lsh_config
        simstore._minhasher = _minhash.MinHasher(n_hashes=lsh_config.n_hashes)
        simstore._lsh = _minhash.LSH(lsh_config, storage=storage)
        return simstore

    @classmethod
    async def _create_object_base(
        cls, storage, storage_level, similarity_threshold, tokenize
    ) -> "SimilarityStore":
        """Create a new SimilarityStore object with the given attributes."""
        obj = SimilarityStore.__new__(cls)
        obj._storage = storage or InMemoryStore()
        obj._storage_level = storage_level
        obj._similarity_threshold = similarity_threshold
        if isinstance(tokenize, str) or tokenize is None:
            obj._tokenize = tokenize or "word_ngrams(3)"
            obj._tokenize_callable = obj._get_tokenize_callable(obj._tokenize)
        else:
            obj._tokenize = "custom"
            obj._tokenize_callable = tokenize
        return obj

    @staticmethod
    def _get_tokenize_callable(tokenize_spec: str):
        """Find the right python function for the given specification as string."""
        match = re.match(r"([a-z_]+)\((.+)\)", tokenize_spec.replace(" ", ""))
        if match and match.group(1) == "word_ngrams":
            return lambda s: _tokenize.word_ngrams(s, n=int(match.group(2)))
        elif match and match.group(1) == "char_ngrams":
            args = match.group(2).split(",")
            n = int(args[0])
            pad_char = None
            if len(args) > 1:
                if (
                    len(args[1]) > 1
                    and args[1][0] == args[1][-1] == '"'
                    or args[1][0] == args[1][-1] == "'"
                ):
                    pad_char = args[1][1:-1]
                else:
                    pad_char = args[1]
            if pad_char:
                return lambda s: _tokenize.char_ngrams(s, n=n, pad_char=pad_char)
            return lambda s: _tokenize.char_ngrams(s, n=n)
        raise ValueError(f"Tokenization function not found: {tokenize_spec}")

    async def _initialize_storage(self):
        """Initialize the internal storage.

        Raises:
            AlreadyInitialized: When the object or the underlying storage had already be
                initialized before.

        Must be called exactly once for a new object. Should not be called when connecting to an
        existing database.
        """
        await self._storage.initialize()
        await self._storage.insert_setting("similarity_threshold", str(self._similarity_threshold))
        await self._storage.insert_setting("storage_level", str(self._storage_level.value))
        await self._storage.insert_setting("tokenize", self._tokenize)
        await self._storage.insert_setting("lsh_config", self._lsh_config.to_json())
        self._minhasher = _minhash.MinHasher(n_hashes=self._lsh_config.n_hashes)
        self._lsh = _minhash.LSH(self._lsh_config, storage=self._storage)

    async def insert(
        self, document: str, *, document_id: int = None, exact_part: str = None, data: str = None
    ) -> int:
        """Index a new document.

        Args:
            document: A document (as string to index).
            document_id: Optional ID to assign to the document.
            exact_part: Optional exact string to match when searching for the document.
            data: Optional additional payload to save together with the document.

        Returns:
            The ID under which the document was indexed.
        """
        tokens = self._tokenize_callable(document)
        fingerprint = self._minhasher.minhash(tokens)
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

    def _filter_candidates(self, candidates, tokens, exact_part) -> List[StoredDocument]:
        """Filter out candidates below the similarity threshold and sort by similarity."""
        candidates = list(filter(lambda c: c.exact_part == exact_part, candidates))
        candidate_tokens = [set(self._tokenize_callable(c.document)) for c in candidates]
        tokens = set(tokens)
        true_jaccards = [_jaccard_similarity(tokens, ct) for ct in candidate_tokens]
        candidates = [
            c
            for jaccard, c in sorted(
                filter(
                    lambda t: t[0] >= self._similarity_threshold, zip(true_jaccards, candidates)
                ),
                key=lambda t: (t[0], t[1].id_ or 0),
                reverse=True,
            )
        ]
        return candidates

    async def query(
        self, document: str, *, exact_part=None, validate: bool = None
    ) -> Collection[StoredDocument]:
        """Query all similar documents.

        Args:
            document: A document for which to search similar items.
            exact_part: Part that should be exactly matched.
            validate: Whether to validate if the results are really above the similarity threshold.
                This is only possible if the storage level is at least "Document". Per default
                validation is done if the data is available, otherwise not.

        Returns:
            A List of :obj:`~narrow_down.storage.StoredDocument` objects with all elements
            which are estimated to be above the similarity threshold.
        """
        tokens = self._tokenize_callable(document)
        fingerprint = self._minhasher.minhash(tokens)
        candidates = await self._lsh.query(fingerprint=fingerprint, exact_part=exact_part)
        if (self._storage_level & StorageLevel.Document) and validate is not False:
            candidates = self._filter_candidates(candidates, tokens, exact_part)
        return candidates

    async def query_top_n(
        self, n: int, document: str, *, exact_part=None, validate: bool = None
    ) -> Collection[StoredDocument]:
        """Query the top n similar documents.

        Args:
            n: The number of similar documents to retrieve.
            document: A document for which to search similar items.
            exact_part: Part that should be exactly matched.
            validate: Whether to validate if the results are really above the similarity threshold.
                This is only possible if the storage level is at least "Document". Per default
                validation is done if the data is available, otherwise not.

        Returns:
            A List of :obj:`~narrow_down.storage.StoredDocument` objects with the n
            elements which are most likely above the similarity threshold.

        Note that the results are probabilistic. The documents are assumed to be the most likely
        candidates if they have the most likely fingerprint. But the actual similarity of the
        documents themselves might differ. However, if `validate` is `True` the ordering of the
        results is correct, because the actual documents are compared with each other.
        """
        tokens = self._tokenize_callable(document)
        fingerprint = self._minhasher.minhash(tokens)
        if (self._storage_level & StorageLevel.Document) and validate is not False:
            # Query 4x the desired number to have some buffer for filtering
            candidates = await self._lsh.query_top_n(
                n=n * 4, fingerprint=fingerprint, exact_part=exact_part
            )
            candidates = self._filter_candidates(candidates, tokens, exact_part)
            return candidates[:n]  # type: ignore
        return await self._lsh.query_top_n(n=n, fingerprint=fingerprint, exact_part=exact_part)


def _jaccard_similarity(s1: Iterable, s2: Iterable):
    if not isinstance(s1, set):
        s1 = set(s1)
    if not isinstance(s2, set):
        s2 = set(s2)
    union = s1.union(s2)
    if not union:
        return 1.0 if len(s1) == len(s2) == 0 else 0.0
    return len(s1.intersection(s2)) / len(union)
