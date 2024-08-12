"""Errors for the SDK."""


class TestCreationError(Exception):
    """
    Exception raised when there is an error creating a test.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
