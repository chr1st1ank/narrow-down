"""Type definitions of pure data classes and abstract types."""
from dataclasses import dataclass
from typing import NewType, Optional

import numpy as np
from numpy import typing as npt

Fingerprint = NewType("Fingerprint", npt.NDArray[np.uint32])
"""Type representing the result of a minhashing operation"""


@dataclass
class StoredDocument:
    """Data object combining all possible fields of a document stored."""

    id_: str
    """Identifier used to distinguish the document from an identical one."""

    document: Optional[str] = None
    """The actual content to use for fuzzy matching, e.g. a full unprocessed sentence."""

    exact_part: Optional[str] = None
    """A string which should be matched exactly."""

    fingerprint: Optional[Fingerprint] = None
    """A fuzzy fingerprint of the document, e.g. a Minhash."""

    data: Optional[str] = None
    """Payload to persist together with the document in the internal data structures."""
