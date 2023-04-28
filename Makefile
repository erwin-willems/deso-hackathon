
SHELL = /bin/bash

.PHONY: help

VIRTUAL_ENV ?= env
bin = ${VIRTUAL_ENV}/bin
requirements = ${VIRTUAL_ENV}/.requirements.installed

# pip and python implicitly provide virtualenv
${bin}/pip: | ${bin}/python
${bin}/python:
	@python3.11 -m venv env

mrproper:
	@rm -rf env

help: ## Displays help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-z0-9A-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

env: ## Create Python environment
	@python3.11 -m venv env

activate-env: ## Activate Python environment
	@. env/bin/activate

test: ## Run pytest
	@pytest --verbose

doc: ## Run pydoc
	@pydoc

lint: ## Run pylint
	@pylint *.py

fix:
	@black *.py
	@isort *.py

dev: setup-dev setup ## Run main.py from working directory
	@export FLASK_ENV=development && python main.py


${bin}/pip-compile ${bin}/pip-sync: | ${bin}/pip
	${bin}/pip install --quiet pip-tools

requirements = ${VIRTUAL_ENV}/.requirements.installed
${requirements}: requirements.txt requirements-dev.txt | ${bin}/pip-sync
	${bin}/pip-sync $^
	@touch $@

requirements: requirements.txt requirements-dev.txt ## Create requirements.txt on first class requirements in .in files.
requirements.txt: %.txt: %.in | ${bin}/pip-compile
	${bin}/pip-compile ${pip_compile_args} --output-file $@ $<

requirements-dev.txt: %.txt: %.in requirements.txt | ${bin}/pip-compile
	${bin}/pip-compile ${pip_compile_args} --output-file $@ $<

setup: ${requirements} ${bin}/python
setup-dev: ${bin}/pip
	${bin}/pip install --requirement requirements-dev.txt

