# D2R Item Analyzer

A Python tool for analyzing Diablo 2: Resurrected items.

## Prerequisites

- Python 3.13+
- Poetry (2.x recommended)

Install Poetry (if needed):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify installation:

```bash
poetry --version
```

## Getting Started

From the project root:

```bash
poetry install --with dev
```

Run the app:

```bash
poetry run d2r-analyzer
```

Or use the Makefile:

```bash
make setup
make run
```

## Common Commands

Install or refresh dependencies:

```bash
poetry install --with dev
```

Run tests:

```bash
poetry run pytest
```

Build source and wheel distributions:

```bash
poetry build
```

Build a single-file executable (PyInstaller):

```bash
make build-exe
```

Note: executable builds currently require Python 3.13 or 3.14 because `pyinstaller` does not yet support Python 3.15+.

## Makefile Targets

- `make setup`: install runtime and dev dependencies via Poetry
- `make install-dev`: alias for `make setup`
- `make run`: run the app via Poetry
- `make build`: build wheel/sdist via Poetry
- `make build-exe`: build one-file executable with PyInstaller
- `make clean`: remove build artifacts (`build/`, `dist/`, and `*.spec`)

## Notes

- Dependencies are managed in `pyproject.toml` with Poetry.
- `requirements.txt` is no longer used.