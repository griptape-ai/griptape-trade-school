.PHONY: install
install: ## Install all dependencies.
	@poetry install --with test --all-extras --no-root

.PHONY: test  ## Run all tests.
test: test/integration

.PHONY: test/integration
test/integration:
	@poetry run pytest -n auto tests/integration/test_code_reviews.py

.PHONY: check
check: check/types check/spell ## Run all checks.

.PHONY: check/types
check/types:
	@poetry run pyright docs/courses/**/code_reviews/*.py
	
.PHONY: check/spell
check/spell:
	@poetry run typos 
	
.PHONY: docs
docs: ## Build documentation.
	@poetry run mkdocs build

.DEFAULT_GOAL := help
.PHONY: help
help: ## Print Makefile help text.
	@# Matches targets with a comment in the format <target>: ## <comment>
	@# then formats help output using these values.
	@grep -E '^[a-zA-Z_\/-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-12s\033[0m%s\n", $$1, $$2}'
