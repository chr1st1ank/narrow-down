use fasthash::murmur3;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn murmur3_32bit(s: &str) -> u32 {
    murmur3::hash32(s)
}

#[pymodule]
fn _rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(murmur3_32bit, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_murmur3_32bit() {
        assert_eq!(murmur3_32bit("test"), 3127628307u32);
        assert_eq!(murmur3_32bit(""), 0u32);
    }
}
