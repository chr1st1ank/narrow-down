use fasthash::{murmur3, xx};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn murmur3_32bit(s: &str) -> u32 {
    murmur3::hash32(s)
}

#[pyfunction]
fn xxhash_32bit(s: &str) -> u32 {
    xx::hash32(s)
}

#[pyfunction]
fn xxhash_64bit(s: &str) -> u64 {
    xx::hash64(s)
}

#[pymodule]
fn _rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(murmur3_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_64bit, m)?)?;
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
