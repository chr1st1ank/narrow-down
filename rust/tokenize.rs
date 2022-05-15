// Rust implementations for narrow_down._tokenize
#![allow(clippy::needless_option_as_deref)]
// use std::collections::HashSet;

use pyo3::ffi::{PySet_Add, PyUnicode_Substring, Py_ssize_t};
use pyo3::prelude::*;
use pyo3::types::{PySet, PyString};
use pyo3::AsPyPointer;

// // Padding. Example for times = 2: "abc" => "$$abc$$"
// fn pad_both_sides(s: &str, pad_char: char, times: usize) -> String {
//     let mut padded = String::with_capacity(s.len() + 2 * times);
//     for _ in 0..(times) {
//         padded.push(pad_char)
//     }
//     padded.push_str(s);
//     for _ in 0..(times) {
//         padded.push(pad_char)
//     }
//     padded
// }
//
// pub fn char_ngrams_unpadded(s: &str, n: usize) -> HashSet<String> {
//     let mut ngrams: HashSet<String> = HashSet::new();
//     let mut iter = s.chars();
//     loop {
//         let ngram = iter.clone().take(n).collect::<String>();
//         if ngram.len() < n {
//             break;
//         }
//         ngrams.insert(ngram);
//         iter.next();
//     }
//
//     ngrams
// }
//
// #[pyfunction]
// pub fn char_ngrams_bytes(s: &str, n: usize, pad_char: Option<char>) -> HashSet<String> {
//     if s.is_empty() {
//         return HashSet::new();
//     }
//     if let Some(c) = pad_char {
//         return char_ngrams_unpadded(pad_both_sides(s, c, n - 1).as_str(), n);
//     } else {
//         return char_ngrams_unpadded(s, n);
//     }
// }

#[pyfunction]
pub fn char_ngrams_str<'py>(
    py: Python<'py>,
    s: &PyString,
    n: usize,
    pad_char: Option<&PyString>,
) -> PyResult<&'py PySet> {
    if s.len().unwrap() == 0 {
        return Ok(PySet::empty(py).unwrap());
    }

    let padded: &PyString = if let Some(c) = pad_char {
        let padding: &PyString = c.call_method1("__mul__", (n - 1,))?.extract()?;
        padding
            .call_method1("__add__", (s,))?
            .extract::<&PyString>()?
            .call_method1("__add__", (padding,))?
            .extract()?
    } else {
        s
    };
    let set = PySet::empty(py).unwrap();
    for i in 0..(padded.len().unwrap() - n + 1) {
        unsafe {
            PySet_Add(
                set.as_ptr(),
                PyUnicode_Substring(padded.as_ptr(), i as Py_ssize_t, (i + n) as Py_ssize_t),
            )
        };
    }
    Ok(set)
}
