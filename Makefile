SHELL := /bin/bash
VENV  ?= .venv
BIN   := $(VENV)/bin
PIP   := $(BIN)/pip
BLACK := $(BIN)/black
COVER := $(BIN)/coverage

.PHONY: help
help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean: clean-db clean-logs
clean-db:
	rm test*.db 2>/dev/null
	rm -rf **/*/__pycache__/ 2>/dev/null

clean-venv:
	rm -rf .venv/ 2>/dev/null

clean-logs:
	rm pysweeper.log

setup: ## Create virtual environment
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

lint: lint-backend ## Lint project
lint-backend: ## Lint backend
	$(BLACK) --check backend/

fmt: fmt-backend ## Format project
fmt-backend: ## Format backend
	$(BLACK) backend/

test: test-backend ## Test project
test-backend: ## Test backend
	$(COVER) run -m unittest discover -s backend/tests
	$(COVER) report -m
