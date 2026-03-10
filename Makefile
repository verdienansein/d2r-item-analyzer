# D2R Item Analyzer build automation (cross-platform, Poetry-managed)
# Usage examples:
#   make setup
#   make run
#   make build
#   make build-exe
#   make clean

# Detect platform-specific options for PyInstaller.
ifeq ($(OS),Windows_NT)
APP_EXT := .exe
PYINSTALLER_PLATFORM_HIDDEN_IMPORTS := \
	--hidden-import pynput.keyboard._win32 \
	--hidden-import pynput.mouse._win32
else
APP_EXT :=
PYINSTALLER_PLATFORM_HIDDEN_IMPORTS :=
endif

ifeq ($(OS),Windows_NT)
POETRY ?= python -m poetry
else
POETRY ?= poetry
endif
APP_NAME := D2RItemAnalyzer
ENTRYPOINT := d2r_analyzer/main.py

.PHONY: help setup install-dev build build-exe run clean lint test sast

help:
	@echo "Targets:"
	@echo "  help        - Show this help message"
	@echo "  lint        - Run ruff for linting and auto-fixing"
	@echo "  test        - Run pytest"
	@echo "  sast        - Run semgrep SAST analysis with security audit rules"
	@echo "  setup       - Install dependencies (including dev tools) with Poetry"
	@echo "  install-dev - Alias for setup"
	@echo "  build       - Build sdist and wheel into dist/"
	@echo "  build-exe   - Build single-file executable via poetry run pyinstaller"
	@echo "  run         - Run app entrypoint via Poetry"
	@echo "  clean       - Remove build artifacts"

lint:
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

test:
	$(POETRY) run pytest

sast:
	$(POETRY) run semgrep --config=p/security-audit .
	$(POETRY) run semgrep --config=p/security-audit --json --output=semgrep-report.json . || true
	@echo "Semgrep SAST report saved to: semgrep-report.json"

setup:
	$(POETRY) install --with dev

install-dev:
	$(POETRY) install --with dev

build:
	$(POETRY) build

build-exe:
	$(POETRY) run pyinstaller \
		--noconfirm \
		--clean \
		--onefile \
		--name $(APP_NAME) \
		$(PYINSTALLER_PLATFORM_HIDDEN_IMPORTS) \
		$(ENTRYPOINT)
	@echo "Binary ready at: dist/$(APP_NAME)$(APP_EXT)"

run:
	$(POETRY) run d2r-analyzer

clean:
	@$(POETRY) run python -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('build', 'dist')]; [p.unlink() for p in pathlib.Path('.').glob('*.spec')]"
