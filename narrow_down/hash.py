"""Hash algorithms."""
from ._rust import murmur3_32bit, xxhash_32bit, xxhash_64bit

__all__ = ["murmur3_32bit", "xxhash_32bit", "xxhash_64bit"]
