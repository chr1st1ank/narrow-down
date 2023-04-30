"""Tests for the `narrow_down.storage` module."""
import dataclasses

import numpy as np
import pytest

from narrow_down.storage import Fingerprint, InMemoryStore, StorageLevel, StoredDocument


@pytest.mark.parametrize("data", [None, "", "user data"])
@pytest.mark.parametrize("fingerprint", [None, Fingerprint(np.array([1]))])
@pytest.mark.parametrize("exact_part", [None, "", "text_exact_part"])
@pytest.mark.parametrize("document", [None, "", "text_document"])
@pytest.mark.parametrize("id_", [None, 0, 1])
@pytest.mark.parametrize(
    "storage_level, expected_fields",
    [
        (StorageLevel.Minimal, {"data"}),
        (StorageLevel.Document, {"data", "document", "exact_part"}),
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
    print("before:", document)
    deserialized = StoredDocument.deserialize(document.serialize(storage_level), id_=None)
    print("after:", deserialized)
    for field in dataclasses.fields(deserialized):
        if field.name in expected_fields:
            assert getattr(deserialized, field.name) == getattr(document, field.name)
        else:
            assert getattr(deserialized, field.name) is None


@pytest.mark.parametrize("data", [None, "", "user data"])
@pytest.mark.parametrize("fingerprint", [None, Fingerprint(np.array([1], dtype=np.uint32))])
@pytest.mark.parametrize("exact_part", [None, "", "text_exact_part"])
@pytest.mark.parametrize("document", [None, "", "text_document"])
@pytest.mark.parametrize("id_", [None, 0, 1])
@pytest.mark.parametrize(
    "storage_level, expected_fields",
    [
        (StorageLevel.Minimal, {"data"}),
        (StorageLevel.Document, {"data", "document", "exact_part"}),
        (StorageLevel.Fingerprint, {"data", "exact_part", "fingerprint"}),
        (StorageLevel.Full, {"data", "document", "exact_part", "fingerprint"}),
    ],
)
def test_stored_document_serialization_rust(
    storage_level, expected_fields, id_, document, exact_part, fingerprint, data
):
    document = StoredDocument(
        id_=id_,
        document=document,
        exact_part=exact_part,
        fingerprint=fingerprint,
        data=data,
    )
    print("before:", document)
    python_result = document.serialize(storage_level)
    rust_result = document.serialize_rust(storage_level)
    assert rust_result == python_result
    assert (
        document.deserialize(python_result, 1)
        == document.deserialize_rust(python_result, 1)
        == document.deserialize(rust_result, 1)
        == document.deserialize_rust(rust_result, 1)
    )


def test_stored_document_without():
    document = StoredDocument(id_=5, document="abcd")
    assert document.without("document") == StoredDocument(id_=5)
    assert document.without("document", "id_") == StoredDocument()
    assert document.without() == document
    assert document.without() is not document


def test_stored_document_eq():
    document1 = StoredDocument(id_=5, document="abcd")
    document2 = StoredDocument(id_=5, document="abcd")
    document3 = StoredDocument(id_=5, document="abcd", exact_part="abcd")
    assert document1 == document2
    assert document1 != document3
    assert document2 != document3


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_setting():
    ims = InMemoryStore()
    await ims.insert_setting(key="k", value="155")
    assert await ims.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__overwrite():
    """Adding a duplicate before to see if that's also handled."""
    ims = InMemoryStore()
    await ims.insert_setting(key="k", value="155")
    await ims.insert_setting(key="k", value="268")
    assert await ims.query_setting("k") == "268"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__no_id():
    ims = InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__remove_document():
    ims = InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"
    await ims.remove_document(id_out)
    with pytest.raises(KeyError):
        assert await ims.query_document(id_out)


@pytest.mark.asyncio
async def test_in_memory_store__query_document__keyerror():
    ims = InMemoryStore()
    with pytest.raises(KeyError):
        await ims.query_document(5)


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__duplicate_doc():
    """Adding a duplicate before to see if that's also handled."""
    ims = InMemoryStore()
    await ims.insert_document(document=b"abcd efgh")
    id_out = await ims.insert_document(document=b"abcd efgh")
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id():
    ims = InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__given_id_duplicate():
    """Adding a duplicate before to see if that's also handled."""
    ims = InMemoryStore()
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    id_out = await ims.insert_document(document=b"abcd efgh", document_id=1234)
    assert id_out == 1234
    assert await ims.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__add_documents_to_bucket_and_query():
    ims = InMemoryStore()
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=20)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=20, document_id=21)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    assert sorted(await ims.query_ids_from_bucket(bucket_id=1, document_hash=20)) == [20, 21]


@pytest.mark.asyncio
async def test_in_memory_store__remove_documents_from_bucket():
    ims = InMemoryStore()

    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []

    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []

    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    await ims.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]
    await ims.remove_id_from_bucket(bucket_id=1, document_hash=10, document_id=10)
    assert list(await ims.query_ids_from_bucket(bucket_id=1, document_hash=10)) == []


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__close_and_reopen():
    """Adding a duplicate before to see if that's also handled."""

    async def insert_setting():
        store = await InMemoryStore().initialize()
        await store.insert_setting(key="k", value="155")
        return store.serialize()

    msgpack = await insert_setting()

    assert isinstance(msgpack, bytes)
    store2 = InMemoryStore.deserialize(msgpack)
    assert await store2.query_setting("k") == "155"


@pytest.mark.asyncio
async def test_in_memory_store__insert_query_document__reopen():
    async def insert_doc():
        store = await InMemoryStore().initialize()
        id_ = await store.insert_document(document=b"abcd efgh")
        return id_, store.serialize()

    id_out, msgpack = await insert_doc()

    assert isinstance(msgpack, bytes)
    store2 = InMemoryStore.deserialize(msgpack)
    assert await store2.query_document(id_out) == b"abcd efgh"


@pytest.mark.asyncio
async def test_in_memory_store__add_documents_to_bucket_and_query__reopen():
    async def insert_doc():
        store = await InMemoryStore().initialize()
        await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)
        return store.serialize()

    msgpack = await insert_doc()

    assert isinstance(msgpack, bytes)
    store2 = InMemoryStore.deserialize(msgpack)
    assert list(await store2.query_ids_from_bucket(bucket_id=1, document_hash=10)) == [10]


@pytest.mark.asyncio
async def test_in_memory_store__to_file_from_file(tmpdir):
    msgpck_file = tmpdir / "store.msgpck"

    store = await InMemoryStore().initialize()
    await store.insert_setting(key="k", value="155")
    id_out = await store.insert_document(document=b"abcd efgh")
    await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    data = store.serialize()
    store.to_file(str(msgpck_file))

    with msgpck_file.open("rb") as f:
        assert data == f.read()

    store2 = InMemoryStore.from_file(str(msgpck_file))

    with msgpck_file.open("wb") as f:
        f.write(data)

    assert (await store2.query_setting("k")) == (await store.query_setting("k")) == "155"
    assert (
        (await store2.query_document(id_out))
        == (await store.query_document(id_out))
        == b"abcd efgh"
    )
    assert (
        list(await store2.query_ids_from_bucket(bucket_id=1, document_hash=10))
        == list(await store.query_ids_from_bucket(bucket_id=1, document_hash=10))
        == [10]
    )


@pytest.mark.asyncio
async def test_in_memory_store__to_file_serialize(tmpdir):
    """Validate to_file and serialize() have identical output."""
    msgpck_file = tmpdir / "store.msgpck"

    store = await InMemoryStore().initialize()
    await store.insert_setting(key="k", value="155")
    await store.insert_document(document=b"abcd efgh")
    await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    data = store.serialize()
    store.to_file(str(msgpck_file))

    with msgpck_file.open("rb") as f:
        assert data == f.read()


@pytest.mark.asyncio
async def test_in_memory_store__from_file__deserialize(tmpdir):
    """Make sure from_file() and deserialize() work the same way."""
    msgpck_file = tmpdir / "store.msgpck"

    store = await InMemoryStore().initialize()
    await store.insert_setting(key="k", value="155")
    await store.insert_document(document=b"abcd efgh")
    await store.add_document_to_bucket(bucket_id=1, document_hash=10, document_id=10)

    store.to_file(str(msgpck_file))
    store2 = InMemoryStore.from_file(str(msgpck_file))
    with msgpck_file.open("rb") as f:
        assert store2.serialize() == InMemoryStore.deserialize(f.read()).serialize()
