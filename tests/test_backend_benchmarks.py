"""Benchmark tests for the different storage backends."""
import asyncio

import pytest

from narrow_down.async_sqlite import AsyncSQLiteStore
from narrow_down.data_types import StorageLevel
from narrow_down.similarity_store import SimilarityStore
from narrow_down.sqlite import SQLiteStore
from narrow_down.storage import InMemoryStore


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "storage_backend, storage_level",
    [
        (InMemoryStore, StorageLevel.Minimal),
        (SQLiteStore, StorageLevel.Minimal),
        (AsyncSQLiteStore, StorageLevel.Minimal),
    ],
)
def test_similarity_store__insert_benchmark(
    benchmark, tmp_path, sample_sentences_french, storage_backend, storage_level
):
    if storage_backend == InMemoryStore:
        storage = storage_backend()
    elif storage_backend == SQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark.db"))
    elif storage_backend == AsyncSQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark_aio.db"))
    simstore = SimilarityStore(storage=storage, storage_level=storage_level)
    asyncio.run(simstore.initialize())

    def f():
        async def async_f():
            for doc in sample_sentences_french:
                await simstore.insert(document=doc)

        asyncio.run(async_f())

    benchmark(f)

    assert asyncio.run(simstore.query(sample_sentences_french[0]))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "storage_backend, storage_level",
    [
        (InMemoryStore, StorageLevel.Minimal),
        (SQLiteStore, StorageLevel.Minimal),
        (AsyncSQLiteStore, StorageLevel.Minimal),
    ],
)
def test_similarity_store__query_benchmark(
    benchmark, tmp_path, sample_sentences_french, storage_backend, storage_level
):
    if storage_backend == InMemoryStore:
        storage = storage_backend()
    elif storage_backend == SQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark.db"))
    elif storage_backend == AsyncSQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark_aio.db"))
    simstore = SimilarityStore(storage=storage, storage_level=storage_level)

    async def init():
        await simstore.initialize()
        for doc in sample_sentences_french:
            await simstore.insert(document=doc)

    asyncio.run(init())

    def f():
        async def async_f():
            i = None
            for doc in sample_sentences_french:
                i = await simstore.query(document=doc)
            return i

        return asyncio.run(async_f())

    i = benchmark(f)

    assert isinstance(i, list)
