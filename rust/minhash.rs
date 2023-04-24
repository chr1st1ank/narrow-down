//! Implementation of the minhash algorithm.
use crate::hash;

use numpy::PyReadonlyArray1;
use peroxide::numerical::integral;
use pyo3::prelude::*;

const MERSENNE_PRIME: u64 = u32::MAX as u64; // mersenne prime (1 << 32) - 1

#[pyfunction]
pub fn minhash(
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

/// Calculate the false-positive probability of a given minhash-LSH configuration
#[pyfunction]
pub fn false_positive_probability(threshold: f64, b: i64, r: i64) -> f64 {
    let _f = |s: f64| -> f64 { 1.0 - f64::powf(1.0 - f64::powf(s, r as f64), b as f64) };

    integral::integrate(_f, (0.0, threshold), integral::Integral::G7K15(1e-8))
}

/// Calculate the false-negative probability of a given minhash-LSH configuration
#[pyfunction]
pub fn false_negative_probability(threshold: f64, b: i64, r: i64) -> f64 {
    let _f = |s: f64| -> f64 { 1.0 - (1.0 - f64::powf(1.0 - f64::powf(s, r as f64), b as f64)) };

    integral::integrate(_f, (threshold, 1.0), integral::Integral::G7K15(1e-8))
}

#[cfg(test)]
mod tests {
    use super::*;
    use assert_approx_eq::assert_approx_eq;

    // More an educational test, but not harmful. We rely on u32::MAX being a prime number.
    #[test]
    fn test_mersenne_prime() {
        assert_eq!(MERSENNE_PRIME, (1 << 32) - 1);
    }

    #[test]
    fn test_false_positive_probability() {
        assert_approx_eq!(false_positive_probability(0.5, 22, 5), 0.048354357923112774);
        assert_approx_eq!(false_positive_probability(0.0, 2, 2), 0.0);
        assert_approx_eq!(false_positive_probability(1.0, 2, 2), 0.46666666666666673);
        assert_approx_eq!(false_positive_probability(0.2, 1, 1), 0.020000000000000004);
        assert_approx_eq!(false_positive_probability(0.2, 1, 10), 0.0);
        assert_approx_eq!(false_positive_probability(0.2, 10, 1), 0.11689994053818183);
    }

    #[test]
    fn test_false_negative_probability() {
        assert_approx_eq!(false_negative_probability(0.5, 22, 5), 0.040500421714996834);
        assert_approx_eq!(false_negative_probability(0.0, 2, 2), 0.5333333333333333);
        assert_approx_eq!(false_negative_probability(1.0, 2, 2), 0.0);
        assert_approx_eq!(false_negative_probability(0.2, 1, 1), 0.32000000000000006);
        assert_approx_eq!(false_negative_probability(0.2, 1, 10), 0.7090909109527272);
        assert_approx_eq!(false_negative_probability(0.2, 10, 1), 0.007809031447272733);
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
