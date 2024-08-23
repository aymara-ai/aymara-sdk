"""Errors for the SDK."""


class TestCreationError(Exception):
    """
    Exception raised when there is an error creating a test.
    """

    __test__ = False

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ScoreRunError(Exception):
    """
    Exception raised when there is an error running a score.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
