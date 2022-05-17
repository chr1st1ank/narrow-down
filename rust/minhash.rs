//! Implementation of the minhash algorithm.
use crate::hash;

use numpy::PyReadonlyArray1;
use pyo3::prelude::*;

const MERSENNE_PRIME: u64 = u32::MAX as u64; // mersenne prime (1 << 32) - 1

#[pyfunction]
pub fn minhash<'py>(
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
        .map(|s| hash::murmur3_32bit(s.as_bytes()) as u64)
        .collect();
    let mut minhashes: Vec<u32> = Vec::new();
    let a_slice = a.as_slice()?;
    let b_slice = b.as_slice()?;

    for (a_i, b_i) in a_slice.iter().zip(b_slice) {
        let minhash: u32 = murmur_hashes
            .iter()
            .map(|h| (u64::from(*a_i) * h + u64::from(*b_i)) % MERSENNE_PRIME)
            .min()
            .unwrap_or(MERSENNE_PRIME) as u32;
        minhashes.push(minhash);
    }

    Ok(minhashes)
}

#[cfg(test)]
mod tests {
    use super::*;

    // More an educational test, but not harmful. We rely on u32::MAX being a prime number.
    #[test]
    fn test_mersenne_prime() {
        assert_eq!(MERSENNE_PRIME, (1 << 32) - 1);
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
