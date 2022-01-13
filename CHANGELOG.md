# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
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

[Unreleased]: https://github.com/chr1st1ank/narrow-down/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/chr1st1ank/narrow-down/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/chr1st1ank/narrow-down/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/chr1st1ank/narrow-down/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/chr1st1ank/narrow-down/compare/releases/tag/v0.1.0
