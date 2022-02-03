/// This module contains a Rust implementation of an in-memory storage backend for LSH.

use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::collections::HashMap;

/// A small struct to use as key for a HashMap
#[derive(PartialEq, Hash, std::cmp::Eq)]
struct BucketKey {
    bucket_id: u32,
    document_hash: u32,
}

/// Python class with the in-memory storage implementation.
#[pyclass]
pub struct RustMemoryStore {
    settings: HashMap<String, String>,
    documents: HashMap<u64, Vec<u8>>,
    buckets: HashMap<BucketKey, Vec<u64>>,
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
        Ok(format!("RustMemoryStore()"))
    }
    fn insert_setting(&mut self, key: String, value: String) {
        self.settings.insert(key, value);
    }
    fn query_setting(&self, key: String) -> Option<&String> {
        self.settings.get(&*key)
    }
    fn insert_document(&mut self, document: Vec<u8>, document_id: Option<u64>) -> u64 {
        if let Some(id) = document_id {
            self.documents.insert(id, document);
            id
        } else {
            let mut id = self.last_doc_id + 1;
            while self.documents.contains_key(&id) {
                id += 1;
            }
            self.last_doc_id = id;
            self.documents.insert(id, document);
            id
        }
    }
    fn query_document<'a>(&self, py: Python<'a>, document_id: u64) -> Option<&'a PyBytes> {
        if let Some(bytes) = self.documents.get(&document_id) {
            Some(PyBytes::new(py, bytes))
        } else {
            None
        }
    }
    fn document_id(&mut self, document_id: u64) {
        self.documents.remove(&document_id);
    }
    fn add_document_to_bucket(&mut self, bucket_id: u32, document_hash: u32, document_id: u64) {
        let documents = self
            .buckets
            .entry(BucketKey {
                bucket_id,
                document_hash,
            })
            .or_insert(Vec::with_capacity(1));
        if documents.iter().find(|x| **x == document_id).is_none() {
            documents.push(document_id);
        }
    }
    fn query_ids_from_bucket(&self, bucket_id: u32, document_hash: u32) -> Vec<u64> {
        self.buckets
            .get(&BucketKey {
                bucket_id,
                document_hash,
            })
            .unwrap_or(&Vec::<u64>::with_capacity(0))
            .clone()
    }
    fn remove_id_from_bucket(&mut self, bucket_id: u32, document_hash: u32, document_id: u64) {
        let maybe_bucket = self.buckets.get_mut(&BucketKey {
            bucket_id,
            document_hash,
        });
        if let Some(bucket) = maybe_bucket {
            let maybe_index_in_bucket = bucket.iter().position(|x| *x == document_id);
            if let Some(index_in_bucket) = maybe_index_in_bucket {
                bucket.swap_remove(index_in_bucket);
            }
        }
    }
}
