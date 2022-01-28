# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
- Storage backend for ScyllaDB, a cassandra-like distributed key-value store.

### Changed
- StoredDocument objects are now serialized with protobuf to increase speed and reduce storage
  consumption.
- Storage queries are done concurrently where possible 
- ScyllaDB sessions are now reused which give a great performance benefit

### Fixed
- Integer overflows in the minhash calculation which reduced the quality of the permutations
  (hash functions). Depending on the input effectively max_uint32 was used instead of a prime number 
  in the modulo calculation.

### Removed
- The backend AsyncSQLiteStore is removed, because it turned out that aiosqlite relies on the user 
  to guarantee that only one coroutine at a time tries writing. Otherwise, a "Database locked" 
  exception is thrown. As the performance was anyway worse than expected it was removed.

## [0.5.0] - 2022-01-17
### Changed
- The SQLite backends take now an init parameter "partitions" which leads to internally
  partitioned tables. This reduces query time by a lot.
- Parameters for SQLite were optimized in order to increase insertion speed and reduce the number
  of disk write operations.

## [0.4.0] - 2022-01-16
### Added
- Synchronous and Asynchronous SQLite storage backend
- Settings of SimilarityStore objects are now saved in the storage backend 
- Deserialization of SimilarityStore from an existing storage backend is now possible

## [0.3.1] - 2022-01-14
### Fixed
- Wrong order of parameters for Minhash LSH in the SimilarityStore class

## [0.3.0] - 2022-01-09
### Added
- Documents can now be removed from the index again with SimilarityStore.remove_by_id()

## [0.2.1] - 2022-01-09
### Fixed
- CI only: Wrong URL of test-pypi

## [0.2.0] - 2022-01-09
### Added
- A rust extension was added and therefore moving the build system to Maturin.
- A Minhash-LSH data structure was implemented.
- Different tokenizers for character- and word-n-grams were implemented.

## [0.1.1] - 2021-12-30

## [0.1.0] - 2021-12-30
### Added
- First release on PyPI.

[Unreleased]: https://github.com/chr1st1ank/narrow-down/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/chr1st1ank/narrow-down/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/chr1st1ank/narrow-down/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/chr1st1ank/narrow-down/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/chr1st1ank/narrow-down/compare/releases/tag/v0.1.0
