from enum import Enum


class ScoreRunStatus(str, Enum):
    FAILED = "failed"
    FINISHED = "finished"
    IMAGE_UPLOADING = "image_uploading"
    RECORD_CREATED = "record_created"
    SCORING = "scoring"

    def __str__(self) -> str:
        return str(self.value)
