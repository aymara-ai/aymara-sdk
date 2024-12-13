from enum import Enum


class ExampleType(str, Enum):
    BAD = "bad"
    GOOD = "good"

    def __str__(self) -> str:
        return str(self.value)
