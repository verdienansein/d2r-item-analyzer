# D2R Item Analyzer

> Press a hotkey on any item tooltip — instantly know if it's worth keeping.

D2R Item Analyzer runs silently in the background while you play Diablo 2: Resurrected.
When you hover over an item and press your configured hotkey, it captures the tooltip,
evaluates the item, and displays a grading overlay directly on your screen.

## What it does
- **Captures** the item tooltip under your cursor via a global hotkey
- **Extracts** all item stats from the screenshot using a vision LLM
- **Grades** the item (S / A / B / C / D) based on configuration rules
- **Displays** a overlay showing the verdict and grading

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
