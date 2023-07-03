.PHONY: help test build
.DEFAULT_GOAL := help

help:
	@cat $(firstword $(MAKEFILE_LIST))

test:
	black --check src
	ruff check src
	pyright src
	pytest tests

build:
	poetry build
