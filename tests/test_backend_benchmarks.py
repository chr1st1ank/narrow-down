"""Benchmark tests for the different storage backends.

An individual benchmark can be run and profiled from the command line with::

    py.test 'tests/test_backend_benchmarks.py::test_similarity_store__insert_25_benchmark[ScyllaDBStore-StorageLevel.Minimal]' --profile --profile-svg
    py.test 'tests/test_backend_benchmarks.py::test_similarity_store__query_25_benchmark[ScyllaDBStore-StorageLevel.Minimal]' --profile --profile-svg
"""  # noqa:     E501
import asyncio

import cassandra.cluster  # type: ignore
import pytest

from narrow_down.async_sqlite import AsyncSQLiteStore
from narrow_down.data_types import StorageLevel
from narrow_down.scylladb import ScyllaDBStore
from narrow_down.similarity_store import SimilarityStore
from narrow_down.sqlite import SQLiteStore
from narrow_down.storage import InMemoryStore


def create_scylla_storage(keyspace: str):
    cluster = cassandra.cluster.Cluster(contact_points=["localhost"], port=9042)
    with cluster.connect() as session:
        session.execute(f"DROP KEYSPACE IF EXISTS {keyspace};")
        session.execute(
            f"CREATE KEYSPACE {keyspace} "
            "WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1} "
            "AND durable_writes = False"
        )
    storage = ScyllaDBStore(
        cluster,
        keyspace=keyspace,
    )
    return storage


@pytest.mark.parametrize(
    "storage_backend, storage_level",
    [
        (InMemoryStore, StorageLevel.Minimal),
        (ScyllaDBStore, StorageLevel.Minimal),
        (SQLiteStore, StorageLevel.Minimal),
        (AsyncSQLiteStore, StorageLevel.Minimal),
    ],
)
def test_similarity_store__insert_25_benchmark(
    benchmark, tmp_path, sample_sentences_french, storage_backend, storage_level
):
    if storage_backend == InMemoryStore:
        storage = storage_backend()
    elif storage_backend == ScyllaDBStore:
        storage = create_scylla_storage("insert_benchmark")
    elif storage_backend == SQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark.db"))
    elif storage_backend == AsyncSQLiteStore:
        storage = storage_backend(str(tmp_path / "insert_benchmark_aio.db"))
    simstore = SimilarityStore(storage=storage, storage_level=storage_level)
    asyncio.run(simstore.initialize())

    def f():
        async def async_f():
            await asyncio.gather(
                *[simstore.insert(document=doc) for doc in sample_sentences_french]
            )

        asyncio.run(async_f())

    benchmark(f)

    assert asyncio.run(simstore.query(sample_sentences_french[0]))


@pytest.mark.parametrize(
    "storage_backend, storage_level",
    [
        (InMemoryStore, StorageLevel.Minimal),
        (ScyllaDBStore, StorageLevel.Minimal),
        (SQLiteStore, StorageLevel.Minimal),
        (AsyncSQLiteStore, StorageLevel.Minimal),
    ],
)
def test_similarity_store__query_25_benchmark(
    benchmark, tmp_path, sample_sentences_french, storage_backend, storage_level
):
    if storage_backend == InMemoryStore:
        storage = storage_backend()
    elif storage_backend == ScyllaDBStore:
        storage = create_scylla_storage("insert_benchmark")
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
