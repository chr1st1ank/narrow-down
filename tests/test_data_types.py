"""Tests for `narrow_down.data_types`."""
import dataclasses

import numpy as np
import pytest

from narrow_down.data_types import Fingerprint, StorageLevel, StoredDocument


@pytest.mark.parametrize("data", [None, "user data"])
@pytest.mark.parametrize("fingerprint", [None, Fingerprint(np.array([1]))])
@pytest.mark.parametrize("exact_part", [None, "text_exact_part"])
@pytest.mark.parametrize("document", [None, "text_document"])
@pytest.mark.parametrize("id_", [None, 0, 1])
@pytest.mark.parametrize(
    "storage_level, expected_fields",
    [
        (StorageLevel.Minimal, {"data"}),
        (StorageLevel.Document, {"data", "document"}),
        (StorageLevel.Fingerprint, {"data", "exact_part", "fingerprint"}),
        (StorageLevel.Full, {"data", "document", "exact_part", "fingerprint"}),
    ],
)
def test_stored_document_serialization(
    storage_level, expected_fields, id_, document, exact_part, fingerprint, data
):
    document = StoredDocument(
        id_=id_,
        document=document,
        exact_part=exact_part,
        fingerprint=fingerprint,
        data=data,
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
