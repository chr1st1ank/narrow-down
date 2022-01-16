"""Tests for `narrow_down.similarity_store`."""
import pytest

import narrow_down.data_types
from narrow_down.data_types import StorageLevel
from narrow_down.similarity_store import SimilarityStore
from narrow_down.sqlite import SQLiteStore


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Document,
        StorageLevel.Full,
    ],
)
async def test_similarity_store__insert_and_query_with_default_settings(storage_level):
    simstore = SimilarityStore(storage_level=storage_level)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id

    if storage_level & StorageLevel.Document:
        assert list(results)[0].document == sample_doc
    else:
        assert list(results)[0].document is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tokenize",
    [
        "word_ngrams(2)",
        "char_ngrams(2)",
        "char_ngrams(2, x)",
        "char_ngrams(2, 'x')",
        'char_ngrams(2, "x")',
        lambda s: s.split(),
    ],
)
async def test_similarity_store__insert_reload_and_query_with_custom_tokenizer(tmp_path, tokenize):
    testfile = str(tmp_path / "test.db")

    async def init_and_insert():
        storage = SQLiteStore(testfile)
        simstore = SimilarityStore(
            storage=storage,
            tokenize=tokenize,
            storage_level=StorageLevel.Document,
        )
        await simstore.initialize()
        return await simstore.insert("Some example document")

    async def load_and_query():
        storage = SQLiteStore(testfile)
        if isinstance(tokenize, str):
            simstore = await SimilarityStore.load_from_storage(storage=storage)
        else:  # Custom tokenizer
            simstore = await SimilarityStore.load_from_storage(storage=storage, tokenize=tokenize)

        return await simstore.query("Some example document")

    doc_id = await init_and_insert()
    results = await load_and_query()

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id
    assert list(results)[0].document == "Some example document"


@pytest.mark.asyncio
async def test_similarity_store__load_from_storage__invalid_storage_level():
    storage = narrow_down.storage.InMemoryStore()
    with pytest.raises(TypeError, match=r"int\(\) argument"):
        await SimilarityStore.load_from_storage(storage)


@pytest.mark.asyncio
async def test_similarity_store__load_from_storage__invalid_lsh_config():
    storage = narrow_down.storage.InMemoryStore()
    await storage.insert_setting("storage_level", "1")
    await storage.insert_setting("tokenize", "char_ngrams(3)")
    with pytest.raises(TypeError, match="lsh_config setting could not be read"):
        await SimilarityStore.load_from_storage(storage)


@pytest.mark.asyncio
async def test_similarity_store__load_from_storage__invalid_tokenize_function():
    storage = narrow_down.storage.InMemoryStore()
    await storage.insert_setting("storage_level", "1")
    await storage.insert_setting("lsh_config", '{"n_hashes": 0, "n_bands": 1, "rows_per_band": 2}')
    await storage.insert_setting("tokenize", "custom")
    with pytest.raises(TypeError, match="tokenize function cannot be deserialized"):
        await SimilarityStore.load_from_storage(storage)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tokenize",
    [
        "word_ngrams(2)",
        "char_ngrams(2)",
        "char_ngrams(2, x)",
        "char_ngrams(2, 'x')",
        'char_ngrams(2, "x")',
    ],
)
async def test_similarity_store__insert_and_query_with_custom_tokenizer(tokenize: str):
    simstore = SimilarityStore(tokenize=tokenize)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id


def test_similarity_store__insert_and_query_with_invalid_tokenizer():
    with pytest.raises(ValueError):
        SimilarityStore(tokenize="x(y)")


@pytest.mark.asyncio
async def test_similarity_store__insert_and_query_with_tokenizer_str():
    simstore = SimilarityStore(tokenize=lambda s: s.split())
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id():
    simstore = SimilarityStore(storage_level=StorageLevel.Fingerprint)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    await simstore.remove_by_id(doc_id)
    await simstore.remove_by_id(doc_id + 1, check_if_exists=False)
    results = await simstore.query(sample_doc)

    assert list(results) == []


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__error_storage_level():
    simstore = SimilarityStore(storage_level=StorageLevel.Minimal)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(narrow_down.data_types.TooLowStorageLevel):
        await simstore.remove_by_id(doc_id)
    results = await simstore.query(sample_doc)

    assert len(results) == 1


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__key_error():
    simstore = SimilarityStore(storage_level=StorageLevel.Fingerprint)
    await simstore.initialize()
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(KeyError):
        await simstore.remove_by_id(doc_id + 1, check_if_exists=True)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
