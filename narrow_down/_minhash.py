"""Implementation of the minhash algorithm.

Source: Leskovec, Rajaraman and Ullman, “Mining of Massive Datasets.”, Chapter 3.
"""
import warnings
from dataclasses import dataclass
from typing import Iterable, List, Optional, Set

import numpy as np
import numpy.typing as npt
from scipy.integrate import quad as integrate

from . import _rust, hash
from .data_types import Fingerprint, StoredDocument
from .storage import StorageBackend

_MERSENNE_PRIME = np.uint32((1 << 32) - 1)


@dataclass(frozen=True)
class MinhashLshConfig:
    """Configuration needed for the Minhash-LSH algorithm."""

    n_hashes: int
    """Number of hash permutations for the minhash part."""

    n_bands: int
    """Number of bands for LSH part."""

    rows_per_band: int
    """Number of rows per band for the LSH part."""


class MinHasher:
    """Classic Minhash algorithm."""

    def __init__(
        self,
        n_hashes: int = 100,
        random_seed: Optional[int] = 42,
    ) -> None:
        """Prepare a Minhash object.

        Args:
            n_hashes: The number of hash permutations to create.
            random_seed: The random seed for hash permutations.
                Pass None to achieve true randomness.

        Raises:
            ValueError: When the given hash_algorithm isn't supported.
        """
        gen = np.random.RandomState(random_seed)
        self.a: npt.NDArray[np.uint32] = gen.randint(
            1, _MERSENNE_PRIME, size=n_hashes, dtype="uint32"
        )
        self.b: npt.NDArray[np.uint32] = gen.randint(
            0, _MERSENNE_PRIME, size=n_hashes, dtype="uint32"
        )

    def minhash(self, shingles: List[str]) -> Fingerprint:
        """Calculate the array of minhashes for a list of strings.

        Args:
            shingles: The parts of the document to hash as list of strings

        Returns:
            A 1xN-dimensional (where N = n_hashes) numpy array of integers which contains the
            minhashes for the input.
        """
        return Fingerprint(
            np.array(  # TODO: Create array directly in Rust
                _rust.minhash(shingle_list=shingles, a=self.a, b=self.b), np.uint32
            )
        )


class LSH:
    """Locality sensitive hash structure to store minhashes efficiently."""

    def __init__(
        self,
        lsh_config: MinhashLshConfig,
        storage: StorageBackend,
    ):
        """Create a new LSH object."""
        self._storage = storage
        self.n_hashes = lsh_config.n_hashes
        self.n_bands = lsh_config.n_bands
        self.rows_per_band = lsh_config.rows_per_band
        self._hashfunc = hash.murmur3_32bit

    def _hash(self, arr: npt.NDArray, exact_part: str = None) -> int:
        """Merge multiple hashes together to one hash."""
        if exact_part:
            return self._hashfunc(bytes(arr.data) + exact_part.encode("utf-8"))
        return self._hashfunc(bytes(arr.data))

    async def insert(
        self,
        fingerprint: Fingerprint,
        *,
        document_id: str = None,
        exact_part: str = None,
        data: str = None,
    ):
        """Index a new document."""
        doc = StoredDocument(exact_part=exact_part, fingerprint=fingerprint, data=data)
        doc_index = await self._storage.insert_document(bytes(doc), document_id=document_id)
        for band_number in range(self.n_bands):
            start_index = band_number * self.rows_per_band
            h = self._hash(fingerprint[start_index : start_index + self.rows_per_band], exact_part)
            await self._storage.add_document_to_bucket(
                bucket_id=band_number, document_hash=h, document_id=doc_index
            )

    async def query(
        self, fingerprint: Fingerprint, *, exact_part: str = None
    ) -> Iterable[StoredDocument]:
        """Find all similar documents."""
        candidates: Set[str] = set()
        for band_number in range(self.n_bands):  # TODO: parallelize
            start_index = band_number * self.rows_per_band
            h = self._hash(fingerprint[start_index : start_index + self.rows_per_band], exact_part)
            candidates.update(
                await self._storage.query_ids_from_bucket(bucket_id=band_number, document_hash=h)
            )
        documents = []
        for c in candidates:  # TODO: Deserialize and make all queries async
            documents.append(StoredDocument.from_bytes(await self._storage.query_document(c)))
        return documents


def find_optimal_config(
    jaccard_threshold: float,
    max_false_negative_proba: float,
    max_false_positive_proba: float,
) -> MinhashLshConfig:
    """Find the optimal configuration given the provided target parameters."""
    num_perm = 2
    b, r = _params_given_false_negative_proba(jaccard_threshold, num_perm, max_false_negative_proba)
    while _false_positive_probability(jaccard_threshold, b, r) > max_false_positive_proba:
        if num_perm >= 16384:
            warnings.warn("Unable to reach error thresholds. Taking the best value.")
            break
        num_perm *= 2
        b, r = _params_given_false_negative_proba(
            jaccard_threshold, num_perm, max_false_negative_proba
        )

    return MinhashLshConfig(n_hashes=num_perm, n_bands=b, rows_per_band=r)


def _params_given_false_negative_proba(
    threshold: float, num_perm: int, max_false_negative_proba: float
):
    for b in range(1, num_perm + 1):
        r = num_perm // b
        fn = _false_negative_probability(threshold, b, r)
        if fn <= max_false_negative_proba:
            return b, r
    warnings.warn(
        "Unable to reach max_false_negative_proba. Taking maximum number of bands to maximize "
        "the number of candidates returned"
    )
    return num_perm, 1


# def _params_given_false_positive_proba(
#     threshold: float, num_perm: int, max_false_positive_proba: float
# ):
#     for b in range(num_perm, 0, -1):
#         r = num_perm // b
#         fp = _false_positive_probability(threshold, b, r)
#         if fp <= max_false_positive_proba:
#             return b, r
#     warnings.warn(
#         "Unable to reach max_false_positive_proba. Taking minimum number of bands to minimize "
#         "false positives"
#     )
#     return 1, num_perm


def _false_positive_probability(threshold: float, b: int, r: int) -> float:
    a, err = integrate(lambda s: 1 - (1 - s ** float(r)) ** float(b), 0.0, threshold)
    return a


def _false_negative_probability(threshold: float, b: int, r: int) -> float:
    a, err = integrate(lambda s: 1 - (1 - (1 - s ** float(r)) ** float(b)), threshold, 1.0)
    return a
