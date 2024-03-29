# Contributing to Narrow Down

👏🎉 First off all, Thanks for your interest in contributing to our project! 🎉👏

The following is a set of guidelines for contributing to Narrow Down. These are
mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

We take our open source community seriously and hold ourselves and other contributors to high standards of communication. By participating and contributing to this project, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Requirements

We use [maturin](https://maturin.rs/) to build the package and install it with dependencies. For development an additional environment manager (e.g. virtualenv, pipenv, miniconda, ...) is sensible to keep the project environment in a dedicated virtual environment. 

With Python's standard venv you can set up the project as follows:
```shell
python -m venv .venv
source ./.venv/bin/activate
python -m pip install --upgrade pip maturin
maturin develop --release --extras dev,docs,scylladb
```

In the project [Task](https://taskfile.dev/) is used to organize tasks like building, testing and more. Please install it separately in order to leverage the automation.
Execute `task -l` to see the list of available commands.

To install the pre-commit hooks:
```shell
pre-commit install
```

## Contributing

### Issues

We use GitHub issues to track public bugs/enhancements. Report a new one by [opening a new issue](https://github.com/chr1st1ank/narrow-down/issues).

In this repository, we provide a couple of templates for you to fill in for:

* Bugs
* Feature Requests/Enhancements

Please read each section in the templates and provide as much information as you can. Please do not put any sensitive information,
such as personally identifiable information, connection strings or cloud credentials. The more information you can provide, the better we can help you.

### Pull Requests

Please follow these steps to have your contribution considered by the maintainers:

1. Fork the repo and create your branch locally with a succinct but descriptive name.
2. Add tests for the new changes
3. Edit documentation if you have changed something significant
4. Make sure to follow the [styleguides](#styleguides)
5. Open a PR in our repository and follow the PR template so that we can efficiently review the changes
6. After you submit your pull request, verify that all status checks are passing

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design
work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Python Code Style

All Python code is linted with [Ruff](https://github.com/charliermarsh/ruff) and formatted with
[Isort](https://github.com/PyCQA/isort) and [Black](https://github.com/psf/black). You can
execute `pre-commit run --all-files` to run the tools.

## Deploying

A reminder for the maintainers on how to deploy.

On branch "main":

- Adjust CHANGELOG.md as described on [https://keepachangelog.com](https://keepachangelog.com).
- Then run `task version -- [major | minor | patch]`. This updates the version numbers and creates a tagged commit.
- Push the commit to github: `git push origin main && git push --tags`
- A github action will automatically create a github release and publish to pypi
