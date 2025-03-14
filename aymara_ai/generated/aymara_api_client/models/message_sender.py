from enum import Enum


class MessageSender(str, Enum):
    AI_UNDER_TEST = "ai_under_test"
    TESTER = "tester"

    def __str__(self) -> str:
        return str(self.value)
