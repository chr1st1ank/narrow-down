use numpy::PyReadonlyArray1;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::hash::Hasher;
use twox_hash::XxHash32;
use twox_hash::XxHash64;

const MERSENNE_PRIME: u64 = u32::MAX as u64; // mersenne prime (1 << 32) - 1

// enum HashAlgorithm {
//     Murmur3_32bit,
//     Xxhash32bit,
//     Xxhash64bit,
// }

/// murmur3_32bit(s: bytes) -> int
/// Calculate the 32 bit murmur3 hash of the input string.
#[pyfunction]
fn murmur3_32bit(s: &[u8]) -> u32 {
    mur3::murmurhash3_x86_32(s, 0)
}

/// xxhash_32bit(s: bytes) -> int
/// Calculate the 32 bit xxhash of the input string.
#[pyfunction]
fn xxhash_32bit(s: &[u8]) -> u32 {
    let mut h = XxHash32::with_seed(0);
    h.write(s);
    h.finish().try_into().unwrap()
}

/// xxhash_64bit(s: bytes) -> int
/// Calculate the 64 bit xxhash of the input string.
#[pyfunction]
fn xxhash_64bit(s: &[u8]) -> u64 {
    let mut h = XxHash64::with_seed(0);
    h.write(s);
    h.finish()
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

    let murmur_hashes: Vec<u64> = shingle_list
        .iter()
        .map(|s| murmur3_32bit(s.as_bytes()) as u64)
        .collect();
    let mut minhashes: Vec<u32> = Vec::new();
    let a_slice = a.as_slice()?;
    let b_slice = b.as_slice()?;
    for (a_i, b_i) in a_slice.iter().zip(b_slice) {
        let minhash: u32 = murmur_hashes
            .iter()
            .map(|h| u64::from(*a_i) * h + u64::from(*b_i) % MERSENNE_PRIME)// TODO
            .min()
            .unwrap_or(MERSENNE_PRIME) as u32;
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

    // More an educational test, but not harmful. We relly on u32::MAX being a prime number.
    #[test]
    fn test_mersenne_prime() {
        assert_eq!(MERSENNE_PRIME, (1 << 32) - 1);
    }

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

    // // This needs linking to libpython and doesn't work with cargo test:
    // use numpy::IntoPyArray;
    // #[test]
    // fn test_minhash() {
    //     Python::with_gil(|py|{
    //         let shingles = vec!["abc", "def"];
    //         let a = vec![1608637543u32, 3421126068u32].into_pyarray(py);
    //         let b = vec![4083286876u32,  787846414u32].into_pyarray(py);
    //         let mh = minhash(py, shingles, a.readonly(), b.readonly());
    //         assert_eq!(mh.unwrap(), vec![530362422u32, 32829942u32]);
    //     });
    // }
}
