//! This module contains a Rust implementation of an in-memory storage backend for LSH.
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyType};
use rustc_hash::{FxHashMap, FxHashSet};
use serde::{Deserialize, Serialize};
use std::fs::File;

/// A small struct to use as key for a HashMap
#[derive(PartialEq, Hash, std::cmp::Eq, Serialize, Deserialize)]
struct BucketKey {
    bucket_id: u32,
    document_hash: u32,
}

/// Python class with the in-memory storage implementation.
#[pyclass]
#[derive(Serialize, Deserialize)]
pub struct RustMemoryStore {
    settings: FxHashMap<String, String>,
    documents: FxHashMap<u64, Vec<u8>>,
    buckets: FxHashMap<BucketKey, FxHashSet<u64>>,
    last_doc_id: u64,
}

#[pymethods]
impl RustMemoryStore {
    #[new]
    fn new() -> Self {
        RustMemoryStore {
            settings: FxHashMap::default(),
            documents: FxHashMap::default(),
            buckets: FxHashMap::default(),
            last_doc_id: 0,
        }
    }
    fn __repr__(&self) -> PyResult<String> {
        let serialized = serde_json::to_string(&self.settings).unwrap();
        Ok(format!(
            "InMemoryStore(size={}, settings={})",
            self.documents.len(),
            serialized
        ))
    }
    fn serialize<'a>(&self, py: Python<'a>) -> PyResult<&'a PyBytes> {
        Ok(PyBytes::new(
            py,
            &rmp_serde::encode::to_vec_named(&self).unwrap(),
        ))
    }
    fn to_file(&self, file_path: &str) {
        let mut f = File::create(file_path).unwrap();
        rmp_serde::encode::write_named(&mut f, self).unwrap();
    }
    #[classmethod]
    fn deserialize(_cls: &PyType, msgpack: &[u8]) -> PyResult<RustMemoryStore> {
        Ok(rmp_serde::from_read_ref(msgpack).unwrap())
    }
    #[classmethod]
    fn from_file(_cls: &PyType, file_path: &str) -> PyResult<RustMemoryStore> {
        let mut f = File::open(file_path).unwrap();
        let obj = rmp_serde::from_read(&mut f).unwrap();
        Ok(obj)
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
    fn remove_document(&mut self, document_id: u64) {
        self.documents.remove(&document_id);
    }
    fn add_document_to_bucket(&mut self, bucket_id: u32, document_hash: u32, document_id: u64) {
        let documents = self
            .buckets
            .entry(BucketKey {
                bucket_id,
                document_hash,
            })
            .or_insert_with(|| FxHashSet::with_capacity_and_hasher(1, Default::default()));
        documents.insert(document_id);
    }
    fn query_ids_from_bucket(&self, bucket_id: u32, document_hash: u32) -> Vec<u64> {
        if let Some(bucket) = self.buckets.get(&BucketKey {
            bucket_id,
            document_hash,
        }) {
            bucket.iter().copied().collect::<Vec<_>>()
        } else {
            Vec::<u64>::with_capacity(0)
        }
    }
    fn remove_id_from_bucket(&mut self, bucket_id: u32, document_hash: u32, document_id: u64) {
        let maybe_bucket = self.buckets.get_mut(&BucketKey {
            bucket_id,
            document_hash,
        });
        if let Some(bucket) = maybe_bucket {
            bucket.remove(&document_id);
        }
    }
}
