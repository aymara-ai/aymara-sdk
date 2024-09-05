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
	@pytest $(test) -s

test-unit:
	@pytest tests/unit/ $(ARGS) $(test)

test-integration:
	@pytest tests/integration/ $(ARGS) -s $(test)


generate-client:
	openapi-python-client generate --url http://localhost:8000/openapi.json --output-path aymara_sdk/generated --overwrite --config aymara_sdk/client_config.yml