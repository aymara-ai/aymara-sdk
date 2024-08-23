from enum import Enum


class TestStatus(str, Enum):
    FAILED = "failed"
    FINISHED = "finished"
    GENERATING_QUESTIONS = "generating_questions"
    RECORD_CREATED = "record_created"

    def __str__(self) -> str:
        return str(self.value)
