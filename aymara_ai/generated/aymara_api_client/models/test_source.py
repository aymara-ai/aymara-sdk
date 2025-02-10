from enum import Enum


class TestSource(str, Enum):
    AYMARA = "aymara"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
