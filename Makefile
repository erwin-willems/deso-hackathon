SHELL = /bin/bash

DOCKER_TAG = data-stream

.PHONY: help


help: ## Displays help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-z0-9A-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)


env: ## Create Python environment
	@python3 -m venv env

activate-env: ## Activate Python environment
	@. env/bin/activate

test: ## Run pytest
	@pytest --verbose

doc: ## Run pydoc
	@pydoc

lint: ## Run pylint
	@pylint *.py

requirements.txt:
	@python3 -m pip freeze > requirements.txt

requirements: requirements.txt ## Make requirements.txt file

fix:
	@isort *.py
	@black *.py

