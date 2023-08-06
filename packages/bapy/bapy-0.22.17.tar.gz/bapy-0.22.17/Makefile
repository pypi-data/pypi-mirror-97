BUMP := patch  # <major|minor|patch>
all: upload
.PHONY: all vars venv clean test
SHELL := $(shell command -v bash)
DIR := $(shell dirname "$(realpath $(firstword $(MAKEFILE_LIST)))")
PROJECT := $(shell basename $(DIR))
COMMAND := source $(DIR)/venv/bin/activate; cd $(DIR)/$(PROJECT);
ACTIVATE := $(DIR)/venv/bin/activate

vars:  ## print Makefile vars
	@echo "BUMP: $(BUMP)"
	@echo "CURRENT: $(CURRENT)"
	@echo "DIR: $(DIR)"
	@echo "PROJECT: $(PROJECT)"
	@echo "PEN: $(PEN)"
	@echo "BAPY: $(BAPY)"


venv:
	@venv.sh
clean:
	@clean.sh

test: clean venv darglint doctest pytest
darglint:
	@bash -c '$(COMMAND) darglint -v 2 -s google --log-level DEBUG --strictness full $(DIR)/$(PROJECT)/*.py'
mypy:
	@bash -c '$(COMMAND) mypy --config-file $(DIR)/setup.cfg --show-traceback $(DIR)/$(PROJECT)/*.py'
doctest:
	@bash -c '$(COMMAND) python -m doctest $(DIR)/$(PROJECT)/*.py  # -v'
pytest:
	@bash -c '$(COMMAND) pytest'

upload: test
	@upload.sh $(BUMP)
