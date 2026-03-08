# D2R Item Analyzer build automation (cross-platform)
# Usage examples:
#   make setup
#   make build
#   make build-exe
#   make run
#   make clean

# Detect platform and use the appropriate virtualenv Python path.
ifeq ($(OS),Windows_NT)
BOOTSTRAP_PYTHON := py -3
PYTHON := .venv/Scripts/python.exe
APP_EXT := .exe
PYINSTALLER_PLATFORM_HIDDEN_IMPORTS := \
	--hidden-import pynput.keyboard._win32 \
	--hidden-import pynput.mouse._win32
else
BOOTSTRAP_PYTHON := python3
PYTHON := .venv/bin/python
APP_EXT :=
PYINSTALLER_PLATFORM_HIDDEN_IMPORTS :=
endif

PIP := $(PYTHON) -m pip
APP_NAME := D2RItemAnalyzer
ENTRYPOINT := d2r_analyzer/main.py

.PHONY: help venv setup install-dev build build-exe run clean

help:
	@echo "Targets:"
	@echo "  venv        - Create .venv if missing"
	@echo "  setup       - Install runtime + build dependencies into .venv"
	@echo "  install-dev - Install package in editable mode"
	@echo "  build       - Build sdist and wheel into dist/"
	@echo "  build-exe   - Build single-file executable with PyInstaller"
	@echo "  run         - Run app entrypoint from .venv"
	@echo "  clean       - Remove build artifacts"

venv:
	$(BOOTSTRAP_PYTHON) -m venv .venv

setup: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	$(PIP) install build pyinstaller

install-dev:
	$(PIP) install -e .

build:
	$(PYTHON) -m build

build-exe:
	$(PYTHON) -m PyInstaller \
		--noconfirm \
		--clean \
		--onefile \
		--name $(APP_NAME) \
		$(PYINSTALLER_PLATFORM_HIDDEN_IMPORTS) \
		$(ENTRYPOINT)
	@echo "Binary ready at: dist/$(APP_NAME)$(APP_EXT)"

run:
	$(PYTHON) -m d2r_analyzer.main

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ('build','dist')]; [p.unlink() for p in pathlib.Path('.').glob('*.spec')]"
