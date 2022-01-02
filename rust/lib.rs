use fasthash::{murmur3, xx};
use numpy::PyReadonlyArray1;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

const MERSENNE_PRIME: u32 = 4294967295u32; // mersenne prime (1 << 32) - 1

enum HashAlgorithm {
    Murmur3_32bit,
    Xxhash32bit,
    Xxhash64bit,
}

/// murmur3_32bit(s: bytes) -> int
/// Calculate the 32 bit murmur3 hash of the input string.
#[pyfunction]
fn murmur3_32bit(s: &[u8]) -> u32 {
    murmur3::hash32(s)
}

/// xxhash_32bit(s: bytes) -> int
/// Calculate the 32 bit xxhash of the input string.
#[pyfunction]
fn xxhash_32bit(s: &[u8]) -> u32 {
    xx::hash32(s)
}

/// xxhash_64bit(s: bytes) -> int
/// Calculate the 64 bit xxhash of the input string.
#[pyfunction]
fn xxhash_64bit(s: &[u8]) -> u64 {
    xx::hash64(s)
}

#[pyfunction]
fn minhash<'py>(
    _py: Python<'py>,
    shingle_list: Vec<&str>,
    a: PyReadonlyArray1<'_, u32>,
    b: PyReadonlyArray1<'_, u32>,
) -> PyResult<Vec<u32>> {
    assert_eq!(a.ndim(), 1);
    assert_eq!(b.ndim(), 1);
    assert_eq!(a.shape()[0], b.shape()[0]);

    let murmur_hashes: Vec<u32> = shingle_list.iter().map(|s| murmur3::hash32(s)).collect();
    let mut minhashes: Vec<u32> = Vec::new();
    let a_slice = a.as_slice()?;
    let b_slice = b.as_slice()?;
    for (a_i, b_i) in a_slice.iter().zip(b_slice) {
        let minhash: u32 = murmur_hashes
            .iter()
            .map(|h| (a_i * h + b_i) % MERSENNE_PRIME)
            .min()
            .unwrap_or(MERSENNE_PRIME);
        minhashes.push(minhash);
    }
    Ok(minhashes)
}

#[pymodule]
fn _rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(murmur3_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_64bit, m)?)?;
    m.add_function(wrap_pyfunction!(minhash, m)?)?;
    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;

    // Test hashes from https://asecuritysite.com/hash/smh
    #[test]
    fn test_murmur3_32bit() {
        assert_eq!(murmur3_32bit("test"), 3127628307u32);
        assert_eq!(murmur3_32bit(""), 0u32);
    }

    #[test]
    fn test_xxhash_32bit() {
        assert_eq!(xxhash_32bit("test"), 1042293711u32);
        assert_eq!(xxhash_32bit(""), 46947589u32);
    }

    #[test]
    fn test_xxhash_64bit() {
        assert_eq!(xxhash_64bit("test"), 5754696928334414137u64);
        assert_eq!(xxhash_64bit(""), 17241709254077376921u64);
    }
}
