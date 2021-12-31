"""Implementation of the minhash algorithm.

Source: Leskovec, Rajaraman, and Ullman, “Mining of Massive Datasets.”, Chapter 3.
"""
from typing import List, Optional

import numpy as np
import numpy.typing as npt

from . import _rust, hash

_MERSENNE_PRIME = np.uint32((1 << 32) - 1)


class MinHash:
    """Classic Minhash algorithm."""

    def __init__(
        self,
        hash_algorithm: hash.HashAlgorithm,
        n_hashes: int = 100,
        random_seed: Optional[int] = 42,
    ) -> None:
        """Prepare a Minhash object.

        Args:
            hash_algorithm: The algorithm to use for hashing
            n_hashes: The number of hash permutations to create
            random_seed: The random seed for hash permutations.
                Pass None to achieve true randomness.
        """
        gen = np.random.RandomState(random_seed)
        self.a = gen.randint(1, _MERSENNE_PRIME, size=n_hashes, dtype="uint32")
        self.b = gen.randint(0, _MERSENNE_PRIME, size=n_hashes, dtype="uint32")

    def hash_str(self, shingles: List[str]) -> npt.NDArray[np.uint32]:
        """Calculate the array of minhashes for a list of strings.

        Args:
            shingles: The parts of the document to hash as list of strings

        Returns:
            A 1xN-dimensional (where N = n_hashes) numpy array of integers which contains the
            minhashes for the input.
        """
        return np.array(  # TODO: Create array directly in Rust
            _rust.minhash(shingle_list=shingles, a=self.a, b=self.b), np.uint32
        )
