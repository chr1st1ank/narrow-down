"""Base classes and interfaces for storage."""
from dataclasses import dataclass
from typing import Optional

import numpy as np
import numpy.typing as npt


@dataclass
class StoredDocument:
    """Data object combining all possible fields of a document stored."""

    id_: str
    """Identifier used to distinguish the document from an identical one."""

    document: Optional[str] = None
    """The actual content to use for fuzzy matching, e.g. a full unprocessed sentence."""

    exact_part: Optional[str] = None
    """A string which should be matched exactly."""

    fingerprint: Optional[npt.NDArray[np.uint32]] = None
    """A fuzzy fingerprint of the document, e.g. a Minhash."""

    data: Optional[str] = None
    """Payload to persist together with the document in the internal data structures."""
