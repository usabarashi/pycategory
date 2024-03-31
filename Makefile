.PHONY: help test build
.DEFAULT_GOAL := help

help:
	@cat $(firstword $(MAKEFILE_LIST))

test:
	poetry run black --check src
	poetry run ruff check src
	poetry run pyright src
	poetry run lint-imports
	poetry run pytest tests

build:
	poetry build
