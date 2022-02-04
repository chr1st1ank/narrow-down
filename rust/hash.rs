//! General purpose hash algorithms
use pyo3::prelude::*;
use std::hash::Hasher;
use twox_hash::XxHash32;
use twox_hash::XxHash64;

/// murmur3_32bit(s: bytes) -> int
/// Calculate the 32 bit murmur3 hash of the input string.
#[pyfunction]
pub fn murmur3_32bit(s: &[u8]) -> u32 {
    mur3::murmurhash3_x86_32(s, 0)
}

/// xxhash_32bit(s: bytes) -> int
/// Calculate the 32 bit xxhash of the input string.
#[pyfunction]
pub fn xxhash_32bit(s: &[u8]) -> u32 {
    let mut h = XxHash32::with_seed(0);
    h.write(s);
    h.finish().try_into().unwrap()
}

/// xxhash_64bit(s: bytes) -> int
/// Calculate the 64 bit xxhash of the input string.
#[pyfunction]
pub fn xxhash_64bit(s: &[u8]) -> u64 {
    let mut h = XxHash64::with_seed(0);
    h.write(s);
    h.finish()
}

#[cfg(test)]
mod tests {
    use super::*;

    // Test hashes from https://asecuritysite.com/hash/smh
    #[test]
    fn test_murmur3_32bit() {
        assert_eq!(murmur3_32bit(b"test"), 3127628307u32);
        assert_eq!(murmur3_32bit(b""), 0u32);
    }

    #[test]
    fn test_xxhash_32bit() {
        assert_eq!(xxhash_32bit(b"test"), 1042293711u32);
        assert_eq!(xxhash_32bit(b""), 46947589u32);
    }

    #[test]
    fn test_xxhash_64bit() {
        assert_eq!(xxhash_64bit(b"test"), 5754696928334414137u64);
        assert_eq!(xxhash_64bit(b""), 17241709254077376921u64);
    }
}
