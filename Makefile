# Makefile in the root directory

# Define the docs directory
DOCS_DIR = docs

# Default target
.PHONY: docs
docs:
	@$(MAKE) -C $(DOCS_DIR) html

# Other common targets
.PHONY: clean
clean:
	@$(MAKE) -C $(DOCS_DIR) clean

.PHONY: help
help:
	@$(MAKE) -C $(DOCS_DIR) help


.PHONY: test
test:
	@pytest

test-unit:
	@pytest tests/unit/

test-integration	:
	@pytest tests/integration/ -s

test-integration-basic:
	@pytest tests/integration/ -s -k "basic"

test-integration-quality:
	@pytest tests/integration/ -s -k "quality"
