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
	@pytest tests/unit/ $(ARGS)

test-integration:
	@pytest tests/integration/ -s $(ARGS)

test-integration-basic:
	@pytest tests/integration/ -s -k "basic" $(ARGS)

test-integration-quality:
	@pytest tests/integration/ -s -k "quality" $(ARGS)
