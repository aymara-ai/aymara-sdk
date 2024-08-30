import sys


def is_notebook() -> bool:
    """Check if the code is running in a Jupyter notebook."""
    return "ipykernel" in sys.modules
