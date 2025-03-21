from enum import Enum


class ConversationStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    STARTED = "started"

    def __str__(self) -> str:
        return str(self.value)
