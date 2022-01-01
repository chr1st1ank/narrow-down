"""Hash algorithms."""
import enum

from ._rust import murmur3_32bit, xxhash_32bit, xxhash_64bit


class HashAlgorithm(enum.Flag):
    """Enum of available hash algorithms."""

    Murmur3_32bit = enum.auto()
    Xxhash_32bit = enum.auto()
    Xxhash_64bit = enum.auto()


_ENUM_TO_FUNCTION = {
    HashAlgorithm.Murmur3_32bit: murmur3_32bit,
    HashAlgorithm.Xxhash_32bit: xxhash_32bit,
    HashAlgorithm.Xxhash_64bit: xxhash_64bit,
}

# __all__ makes Sphinx document the imported rust functions as part of the public API
__all__ = [
    "HashAlgorithm",
    "murmur3_32bit",
    "xxhash_32bit",
    "xxhash_64bit",
]
