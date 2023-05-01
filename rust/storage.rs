use std::io::Cursor;

use numpy::PyArray1;
use numpy::PyReadonlyArray1;
use prost::Message;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict};

mod stored_document {
    include!(concat!(env!("OUT_DIR"), "/stored_document.rs"));
}

/// Create a StoredDocumentProto message from the inputs and return it as bytes object.
#[pyfunction]
pub fn stored_document_to_protobuf(
    py: Python,
    document: Option<String>,
    exact_part: Option<String>,
    fingerprint: Option<PyReadonlyArray1<'_, u32>>,
    data: Option<String>,
) -> PyObject {
    let fingerprint_rust = match fingerprint {
        Some(array) => array.to_vec().unwrap(), // TODO: unsafe
        None => Vec::new(),
    };
    let pb_doc = stored_document::StoredDocumentProto {
        id: None,
        document: document,
        exact_part: exact_part,
        fingerprint: fingerprint_rust,
        data: data,
    };

    PyBytes::new(py, &pb_doc.encode_to_vec()).into()
}

/// Parse a binary StoredDocumentProto message and return its contents as Python dictionary.s
#[pyfunction]
pub fn protobuf_to_stored_document<'py>(py: Python<'py>, document: &[u8]) -> PyResult<&'py PyDict> {
    let buf = Cursor::new(document);
    let pb_doc = stored_document::StoredDocumentProto::decode(buf).unwrap();

    let result_dict = PyDict::new(py);
    if let Some(x) = pb_doc.document {
        result_dict.set_item("document", x).unwrap();
    }
    if let Some(x) = pb_doc.exact_part {
        result_dict.set_item("exact_part", x).unwrap();
    }
    if !pb_doc.fingerprint.is_empty() {
        result_dict
            .set_item("fingerprint", PyArray1::from_vec(py, pb_doc.fingerprint))
            .unwrap();
    }
    if let Some(x) = pb_doc.data {
        result_dict.set_item("data", x).unwrap();
    }
    Ok(result_dict)
}
