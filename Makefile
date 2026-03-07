# D2R Item Analyzer build automation (Windows-friendly)
# Usage examples:
#   make setup
#   make build
#   make build-exe
#   make run
#   make clean

PYTHON := .venv/Scripts/python.exe
PIP := $(PYTHON) -m pip
APP_NAME := D2RItemAnalyzer
ENTRYPOINT := d2r_analyzer/main.py

.PHONY: help setup install-dev build build-exe run clean

help:
	@echo "Targets:"
	@echo "  setup       - Install build dependencies into .venv"
	@echo "  install-dev - Install package in editable mode"
	@echo "  build       - Build sdist and wheel into dist/"
	@echo "  build-exe   - Build single-file Windows executable with PyInstaller"
	@echo "  run         - Run app entrypoint from .venv"
	@echo "  clean       - Remove build artifacts"

setup:
	$(PIP) install --upgrade pip
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
		--hidden-import pynput.keyboard._win32 \
		--hidden-import pynput.mouse._win32 \
		$(ENTRYPOINT)
	@echo "EXE ready at: dist/$(APP_NAME).exe"

run:
	$(PYTHON) -m d2r_analyzer.main

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ('build','dist')]; [p.unlink() for p in pathlib.Path('.').glob('*.spec')]"
