from enum import Enum


class TestType(str, Enum):
    __test__ = False
    HALLUCINATION = "hallucination"
    JAILBREAK = "jailbreak"
    SAFETY = "safety"

    def __str__(self) -> str:
        return str(self.value)
