"""Type hints for the rust library.

The actual code is in the folder /rust.
"""
from typing import Iterable, List, Optional, Set, Union

import numpy as np
import numpy.typing as npt

class RustMemoryStore:
    num: int
    def serialize(self) -> bytes: ...
    def to_file(self, file_path: str): ...
    @classmethod
    def deserialize(cls, msgpack: bytes) -> "RustMemoryStore": ...
    @classmethod
    def from_file(cls, file_path: str) -> "RustMemoryStore": ...
    def insert_setting(self, key: str, value: str): ...
    def query_setting(self, key: str) -> Optional[str]: ...
    def insert_document(self, document: bytes, document_id: int = None) -> int: ...
    def query_document(self, document_id: int) -> bytes: ...
    def remove_document(self, document_id: int): ...
    def add_document_to_bucket(self, bucket_id: int, document_hash: int, document_id: int): ...
    def query_ids_from_bucket(self, bucket_id, document_hash: int) -> Iterable[int]: ...
    def remove_id_from_bucket(self, bucket_id: int, document_hash: int, document_id: int): ...

def murmur3_32bit(s: Union[str, bytes]) -> int: ...
def xxhash_32bit(s: Union[str, bytes]) -> int: ...
def xxhash_64bit(s: Union[str, bytes]) -> int: ...
def minhash(
    shingle_list: List[str], a: npt.NDArray[np.uint32], b: npt.NDArray[np.uint32]
) -> npt.NDArray[np.uint32]: ...
def char_ngrams_str(s: str, n: int, pad_char: Optional[str] = "$") -> Set[str]: ...
