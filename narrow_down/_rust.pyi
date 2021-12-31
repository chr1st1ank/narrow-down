"""Type hints for the rust library.

The actual code is in the folder /rust.
"""
from typing import List

import numpy as np
import numpy.typing as npt

def murmur3_32bit(s: str) -> int: ...
def xxhash_32bit(s: str) -> int: ...
def xxhash_64bit(s: str) -> int: ...
def minhash(
    shingle_list: List[str], a: npt.NDArray[np.uint32], b: npt.NDArray[np.uint32]
) -> npt.NDArray[np.uint32]: ...
