// Rust implementations for narrow_down._tokenize
#![allow(clippy::needless_option_as_deref)]

use pyo3::ffi::{PySet_Add}; //, PyUnicode_Substring, Py_ssize_t};
// use pyo3::ffi::{PySet_Add, PyUnicode_Substring, Py_ssize_t};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PySet};//, PyString};
use pyo3::AsPyPointer;

/// Return the byte vector with a padding of pad_char, repeated "times" times
///
/// # Examples
/// times = 2: "abc" => "$$abc$$"
fn pad_both_sides(s: &[u8], pad_char: u8, times: usize) -> Vec<u8> {
    let mut padded = Vec::with_capacity(s.len() + 2 * times);
    for _ in 0..(times) {
        padded.push(pad_char)
    }
    padded.extend_from_slice(s);
    for _ in 0..(times) {
        padded.push(pad_char)
    }
    padded
}

/// Returns all byte n-grams of length n as Python set
#[pyfunction]
pub fn char_ngrams_bytes<'py>(
    py: Python<'py>,
    s: &[u8],
    n: usize,
    pad_char: Option<&[u8]>,
) -> &'py PySet {
    let set = PySet::empty(py).unwrap();
    if s.is_empty() {
        return set;
    }
    if let Some(c) = pad_char {
        byte_ngrams_unpadded(py, pad_both_sides(s, c[0], n - 1).as_slice(), n, set)
    } else {
        byte_ngrams_unpadded(py, s, n, set)
    }
}

fn byte_ngrams_unpadded<'py>(py: Python, padded: &[u8], n: usize, set: &'py PySet) -> &'py PySet {
    let mut iter = padded.iter();
    loop {
        let ngram = iter.clone().take(n).copied().collect::<Vec<u8>>();
        if ngram.len() < n {
            break;
        }
        let ngram_py = PyBytes::new(py, ngram.as_slice());
        unsafe { PySet_Add(set.as_ptr(), ngram_py.as_ptr()) };
        iter.next();
    }
    set
}

// /// Returns all character n-grams of length n as Python set
// #[pyfunction]
// pub fn char_ngrams_str<'py>(
//     py: Python<'py>,
//     s: &PyString,
//     n: usize,
//     pad_char: Option<&PyString>,
// ) -> PyResult<&'py PySet> {
//     let ngrams = PySet::empty(py).unwrap();
//
//     if s.len().unwrap() == 0 {
//         return Ok(ngrams);
//     }
//
//     let padded: &PyString = if let Some(c) = pad_char {
//         let padding: &PyString = c.call_method1("__mul__", (n - 1,))?.extract()?;
//         padding
//             .call_method1("__add__", (s,))?
//             .extract::<&PyString>()?
//             .call_method1("__add__", (padding,))?
//             .extract()?
//     } else {
//         s
//     };
//
//     for i in 0..(padded.len().unwrap() - n + 1) {
//         unsafe {
//             PySet_Add(
//                 ngrams.as_ptr(),
//                 PyUnicode_Substring(padded.as_ptr(), i as Py_ssize_t, (i + n) as Py_ssize_t),
//             )
//         };
//     }
//
//     Ok(ngrams)
// }
