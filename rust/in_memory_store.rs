use pyo3::prelude::*;
use std::collections::HashMap;
use pyo3::types::PyBytes;

#[pyclass]
pub struct RustMemoryStore {
    settings: HashMap<String, String>,
    documents: HashMap<u64, Vec<u8>>,
    buckets: HashMap<u64, HashMap<u64, Vec<u64>>>,
    last_doc_id: u64,
}

#[pymethods]
impl RustMemoryStore {
    #[new]
    fn new() -> Self {
        RustMemoryStore {
            settings: HashMap::new(),
            documents: HashMap::new(),
            buckets: HashMap::new(),
            last_doc_id: 0,
        }
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("RustMemoryStore()"))    // TODO: Better representation
    }
    fn insert_setting(&mut self, key: String, value: String) {
        self.settings.insert(key, value);
    }
    fn query_setting(&self, key: String) -> Option<&String> {
        self.settings.get(&*key)
    }
    fn insert_document(&mut self, document: Vec<u8>, document_id: Option<u64>) -> u64 {
        let doc_id = match document_id {
            Some(id) => id,
            None => {
                let mut index_candidate = self.last_doc_id + 1;
                while self.documents.contains_key(&index_candidate) {
                    index_candidate += 1;
                }
                self.last_doc_id = index_candidate;
                index_candidate
            },
        };
        self.documents.insert(doc_id, document);
        doc_id
    }
    fn query_document<'a>(&self, py: Python<'a>, document_id: u64) -> Option<&'a PyBytes> {
        if let Some(bytes) = self.documents.get(&document_id) {
            return Some(PyBytes::new(py, bytes));
        }
        None
    }
    fn document_id(&mut self, document_id: u64) {
        self.documents.remove(&document_id);
    }
    fn add_document_to_bucket(&mut self, bucket_id: u64, document_hash: u64, document_id: u64) {
        // TODO: u32
        self.buckets
            .entry(bucket_id)
            .or_insert(HashMap::new())
            .entry(document_hash)
            .or_insert(Vec::new())
            .push(document_id);
    }
    fn query_ids_from_bucket(&self, bucket_id: u64, document_hash: u64) -> Vec<u64> {
        self.buckets
            .get(&bucket_id)
            .unwrap_or(&HashMap::new())
            .get(&document_hash)
            .unwrap_or(&Vec::<u64>::new()).clone()
    }
    fn remove_id_from_bucket(&mut self, bucket_id: u64, document_hash: u64, document_id: u64) {
        // TODO: u32
        let maybe_bucket = self
            .buckets
            .entry(bucket_id)
            .or_insert(HashMap::new())
            .get_mut(&document_hash);
        if let Some(bucket) = maybe_bucket {
            let maybe_index_in_bucket = bucket.iter().position(|x| *x == document_id);
            if let Some(index_in_bucket) = maybe_index_in_bucket {
                bucket.swap_remove(index_in_bucket);
            }
        }
    }
}
