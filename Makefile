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

# Catch-all target: forward all unknown targets to Sphinx makefile
%:
	@$(MAKE) -C $(DOCS_DIR) $@