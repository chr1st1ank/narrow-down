
# Narrow Down


<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/narrow-down.svg)](https://pypi.python.org/pypi/narrow-down)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/narrow-down.svg)](https://pypi.python.org/pypi/narrow-down)
[![Tests](https://github.com/chr1st1ank/narrow-down/workflows/tests/badge.svg)](https://github.com/chr1st1ank/narrow-down/actions?workflow=tests)
[![Codecov](https://codecov.io/gh/chr1st1ank/narrow-down/branch/main/graph/badge.svg)](https://codecov.io/gh/chr1st1ank/narrow-down)
[![Read the Docs](https://readthedocs.org/projects/narrow-down/badge/)](https://narrow-down.readthedocs.io/)
[![PyPI - License](https://img.shields.io/pypi/l/narrow-down.svg)](https://pypi.python.org/pypi/narrow-down)

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)

</div>


Fast fuzzy text search


* GitHub repo: <https://github.com/chr1st1ank/narrow-down.git>
* Documentation: <https://narrow-down.readthedocs.io>
* Free software: Apache Software License 2.0
* Status: Prototype. Solid and fast production quality, but *still subject to API changes until version 1.0 is reached*.


## Features

* Document indexing and search based on the Minhash LSH algorithm
* High performance thanks to a native extension module in Rust
* Easy-to-use API with automated parameter tuning
* Works with many storage backends. Currently implemented:
  * In-Memory
  * SQLite
  * Custom backend by implementing a lean interface
* Native asyncio interface

## Quickstart

TODO

## Similar projects
- [pylsh](https://github.com/mattilyra/LSH) offers a good implementation of the classic Minhash LSH scheme in Python and Cython. If you only need this and you don't need a database backend it can be a good choice.
- [Datasketch](https://github.com/ekzhu/datasketch) implements an interesting collection of different data sketching algorithms for similarity matching, cardinality estimation and k-nearest-neighbour search. The implementation is not highly optimized but very well usable, the documentation rich and multiple database backends can be used for some of the sketches
- [Milvus](https://milvus.io/) offers a full database stack for vector search, a different approach for fast searching. It can also be applied to text search when an emedding like Word2Vec or Bert is used to vectorize the text.

## Credits

This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
