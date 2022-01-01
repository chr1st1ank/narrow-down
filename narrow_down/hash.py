"""Hash algorithms."""
from collections.abc import Callable
from enum import Enum

from ._rust import murmur3_32bit, xxhash_32bit, xxhash_64bit


class HashAlgorithm(Enum):
    """Enum of available hash algorithms."""

    Murmur3_32bit = 1
    # Not yet implemented:
    Xxhash_32bit = 2
    Xxhash_64bit = 3


_ENUM_TO_FUNCTION = {
    HashAlgorithm.Murmur3_32bit: murmur3_32bit,
    HashAlgorithm.Xxhash_32bit: xxhash_32bit,
    HashAlgorithm.Xxhash_64bit: xxhash_64bit,
}


def get_function_by_name(algorithm: HashAlgorithm) -> Callable:
    """Get a hash function corresponding to an enum value."""
    return _ENUM_TO_FUNCTION[algorithm]


# __all__ = ["HashAlgorithm", "murmur3_32bit", "xxhash_32bit", "xxhash_64bit"]
