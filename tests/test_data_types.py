"""Tests for `narrow_down.data_types`."""
import dataclasses

import numpy as np
import pytest

from narrow_down.data_types import Fingerprint, StorageLevel, StoredDocument


@pytest.mark.parametrize(
    "storage_level, expected_fields",
    [
        (StorageLevel.Minimal, {"data"}),
        (StorageLevel.Document, {"data", "document"}),
        (StorageLevel.Fingerprint, {"data", "exact_part", "fingerprint"}),
        (StorageLevel.Full, {"data", "document", "exact_part", "fingerprint"}),
    ],
)
def test_stored_document_serialization(storage_level, expected_fields):
    document = StoredDocument(
        id_=5,
        document="abcd",
        exact_part="exact:part",
        fingerprint=Fingerprint(np.array([1])),
        data="user data",
    )
    deserialized = StoredDocument.deserialize(document.serialize(storage_level), id_=None)
    for field in dataclasses.fields(deserialized):
        if field.name in expected_fields:
            assert getattr(deserialized, field.name) == getattr(document, field.name)
        else:
            assert getattr(deserialized, field.name) is None


def test_stored_document_without():
    document = StoredDocument(id_=5, document="abcd")
    assert document.without("document") == StoredDocument(id_=5)
    assert document.without("document", "id_") == StoredDocument()
    assert document.without() == document
    assert document.without() is not document
