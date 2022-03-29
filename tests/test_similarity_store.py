"""Tests for `narrow_down.similarity_store`."""
import pytest

import narrow_down.storage
from narrow_down.similarity_store import SimilarityStore
from narrow_down.sqlite import SQLiteStore
from narrow_down.storage import StorageLevel, StoredDocument


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
    simstore = await SimilarityStore.create(storage_level=storage_level)
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
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Document,
    ],
)
async def test_similarity_store__compare_query_and_query_top_1(storage_level):
    simstore = await SimilarityStore.create(storage_level=storage_level)
    sample_doc = "Some example document"

    await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)
    results_top_1 = await simstore.query_top_n(n=1, document=sample_doc)

    assert results == results_top_1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "validate",
    [True, False, None],
)
@pytest.mark.parametrize(
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Fingerprint,
        StorageLevel.Document,
        StorageLevel.Full,
    ],
)
async def test_similarity_store__query_with_validation(monkeypatch, storage_level, validate):
    fake_results = [
        StoredDocument(id_=1, document="XYZ", exact_part="A"),
        StoredDocument(id_=2, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="B"),
        StoredDocument(id_=3, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ1", exact_part="A"),
        StoredDocument(id_=4, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ12", exact_part="A"),
        StoredDocument(id_=5, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
        StoredDocument(id_=6, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
    ]

    async def fake_query(*args, **kwargs):
        return fake_results

    simstore = await SimilarityStore.create(storage_level=storage_level, tokenize="char_ngrams(1)")
    monkeypatch.setattr(simstore._lsh, "query", fake_query)

    results = await simstore.query(
        document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A", validate=validate
    )

    print(results)
    if validate is not False and (storage_level & StorageLevel.Document):
        assert results == [
            StoredDocument(id_=6, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
            StoredDocument(id_=5, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
            StoredDocument(id_=3, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ1", exact_part="A"),
            StoredDocument(id_=4, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ12", exact_part="A"),
        ]
    else:
        assert results == fake_results


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "validate",
    [True, False, None],
)
@pytest.mark.parametrize(
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Fingerprint,
        StorageLevel.Document,
        StorageLevel.Full,
    ],
)
async def test_similarity_store__query_top_n_with_validation(monkeypatch, validate, storage_level):
    fake_results = [
        StoredDocument(id_=1, document="XYZ", exact_part="A"),
        StoredDocument(id_=2, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="B"),
        StoredDocument(id_=3, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ1", exact_part="A"),
        StoredDocument(id_=4, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ12", exact_part="A"),
        StoredDocument(id_=5, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
    ]

    async def fake_query(*args, **kwargs):
        return fake_results

    async def fake_query_top_n(n, *args, **kwargs):
        return fake_results[:n]

    simstore = await SimilarityStore.create(storage_level=storage_level, tokenize="char_ngrams(1)")
    monkeypatch.setattr(simstore._lsh, "query", fake_query)
    monkeypatch.setattr(simstore._lsh, "query_top_n", fake_query_top_n)

    results = await simstore.query_top_n(
        n=2, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A", validate=validate
    )

    print(results)
    if validate is not False and (storage_level & StorageLevel.Document):
        assert results == [
            StoredDocument(id_=5, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="A"),
            StoredDocument(id_=3, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ1", exact_part="A"),
        ]
    else:
        assert results == [
            StoredDocument(id_=1, document="XYZ", exact_part="A"),
            StoredDocument(id_=2, document="ABCDEFGHIJKLMNOPQRSTUVWXYZ", exact_part="B"),
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "storage_level",
    [
        StorageLevel.Minimal,
        StorageLevel.Document,
    ],
)
async def test_similarity_store__insert_and_query_top_n(storage_level):
    simstore = await SimilarityStore.create(storage_level=storage_level, tokenize="char_ngrams(1)")
    sample_doc = "Some long example document. An impressive text."

    id1 = await simstore.insert(sample_doc)
    id2 = await simstore.insert(sample_doc + "1")
    await simstore.insert(sample_doc + "12")
    await simstore.insert(sample_doc + "123")

    results_top_n = [d.id_ for d in await simstore.query_top_n(n=1, document=sample_doc)]
    assert results_top_n == [id1]

    results_top_n = [d.id_ for d in await simstore.query_top_n(n=2, document=sample_doc)]
    assert results_top_n == [id1, id2]


def test_similarity_store_warns_on_init():
    with pytest.warns(UserWarning):
        SimilarityStore()


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
        simstore = await SimilarityStore.create(
            storage=storage,
            tokenize=tokenize,
            storage_level=StorageLevel.Document,
        )
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
    await storage.insert_setting("similarity_threshold", "0.8")
    with pytest.raises(TypeError, match=r"int\(\) argument"):
        await SimilarityStore.load_from_storage(storage)


@pytest.mark.asyncio
async def test_similarity_store__load_from_storage__invalid_lsh_config():
    storage = narrow_down.storage.InMemoryStore()
    await storage.insert_setting("storage_level", "1")
    await storage.insert_setting("similarity_threshold", "0.8")
    await storage.insert_setting("tokenize", "char_ngrams(3)")
    with pytest.raises(TypeError, match="lsh_config setting could not be read"):
        await SimilarityStore.load_from_storage(storage)


@pytest.mark.asyncio
async def test_similarity_store__load_from_storage__invalid_tokenize_function():
    storage = narrow_down.storage.InMemoryStore()
    await storage.insert_setting("storage_level", "1")
    await storage.insert_setting("similarity_threshold", "0.8")
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
    simstore = await SimilarityStore.create(tokenize=tokenize)
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id


@pytest.mark.asyncio
async def test_similarity_store__insert_and_query_with_invalid_tokenizer():
    with pytest.raises(ValueError):
        await SimilarityStore.create(tokenize="x(y)")


@pytest.mark.asyncio
async def test_similarity_store__insert_and_query_with_tokenizer_str():
    simstore = await SimilarityStore.create(tokenize=lambda s: s.split())
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
    assert list(results)[0].id_ == doc_id


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id():
    simstore = await SimilarityStore.create(storage_level=StorageLevel.Fingerprint)
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    await simstore.remove_by_id(doc_id)
    await simstore.remove_by_id(doc_id + 1, check_if_exists=False)
    results = await simstore.query(sample_doc)

    assert list(results) == []


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__error_storage_level():
    simstore = await SimilarityStore.create(storage_level=StorageLevel.Minimal)
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(narrow_down.storage.TooLowStorageLevel):
        await simstore.remove_by_id(doc_id)
    results = await simstore.query(sample_doc)

    assert len(results) == 1


@pytest.mark.asyncio
async def test_similarity_store__remove_by_id__key_error():
    simstore = await SimilarityStore.create(storage_level=StorageLevel.Fingerprint)
    sample_doc = "Some example document"

    doc_id = await simstore.insert(sample_doc)
    with pytest.raises(KeyError):
        await simstore.remove_by_id(doc_id + 1, check_if_exists=True)
    results = await simstore.query(sample_doc)

    assert len(results) == 1
