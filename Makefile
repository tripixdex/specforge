PYTHON ?= python3

.PHONY: install test lint demo api ui

install:
	$(PYTHON) -m pip install --no-build-isolation -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

demo:
	$(PYTHON) -m specforge.cli demo

api:
	$(PYTHON) -m uvicorn specforge.api.app:app --reload

ui:
	$(PYTHON) -m uvicorn specforge.api.app:app --reload
