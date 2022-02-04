//! Compiling the library to a Python package
mod hash;
mod in_memory_store;
mod minhash;

use hash::*;
use minhash::*;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pymodule]
fn _rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(murmur3_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_32bit, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_64bit, m)?)?;
    m.add_function(wrap_pyfunction!(minhash, m)?)?;
    m.add_class::<in_memory_store::RustMemoryStore>()?;
    Ok(())
}
