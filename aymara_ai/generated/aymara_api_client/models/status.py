from enum import Enum


class Status(str, Enum):
    CREATED = "created"
    FAILED = "failed"
    FINISHED = "finished"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
