# Makefile in the root directory

# Define the docs directory
DOCS_DIR = docs

# Default target
.PHONY: docs
docs:
	@cp aymara_ai/examples/safety/safety_notebook.ipynb $(DOCS_DIR)/source/
	@cp aymara_ai/examples/safety/free_trial_notebook.ipynb $(DOCS_DIR)/source/
	@cp aymara_ai/examples/jailbreak/jailbreak_notebook.ipynb $(DOCS_DIR)/source/
	@$(MAKE) -C $(DOCS_DIR) html
	@rm $(DOCS_DIR)/source/safety_notebook.ipynb
	@rm $(DOCS_DIR)/source/free_trial_notebook.ipynb
	@rm $(DOCS_DIR)/source/jailbreak_notebook.ipynb

# Other common targets
.PHONY: clean
clean:
	@$(MAKE) -C $(DOCS_DIR) clean

.PHONY: help
help:
	@$(MAKE) -C $(DOCS_DIR) help


.PHONY: test
test:
	@pytest $(case) -s

test-unit:
	@pytest tests/unit/ $(case)

test-integration:
	@pytest tests/integration/ -s $(case)


generate-client:
	openapi-python-client generate --url http://localhost:8000/openapi.json --output-path aymara_ai/generated --overwrite --config aymara_ai/client_config.yml