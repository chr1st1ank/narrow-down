//! Compiling the library to a Python package
mod hash;
mod in_memory_store;
mod minhash;
mod tokenize;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pymodule]
fn _rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(hash::murmur3_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(hash::xxhash_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(hash::xxhash_64bit, m)?)?;
    m.add_function(wrap_pyfunction!(minhash::minhash, m)?)?;
    m.add_function(wrap_pyfunction!(minhash::false_negative_probability, m)?)?;
    m.add_function(wrap_pyfunction!(minhash::false_positive_probability, m)?)?;
    m.add_function(wrap_pyfunction!(tokenize::char_ngrams_bytes, m)?)?;
    // m.add_function(wrap_pyfunction!(tokenize::char_ngrams_str, m)?)?;
    m.add_class::<in_memory_store::RustMemoryStore>()?;
    Ok(())
}
