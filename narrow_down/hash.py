"""Hash algorithms."""
from enum import Enum

from ._rust import murmur3_32bit, xxhash_32bit, xxhash_64bit


class HashAlgorithm(Enum):
    """Enum of available hash algorithms."""

    Murmur3_32bit = 1
    # Not yet implemented:
    # Xxhash32bit = 2
    # Xxhash64bit = 3


__all__ = ["HashAlgorithm", "murmur3_32bit", "xxhash_32bit", "xxhash_64bit"]
