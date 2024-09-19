from enum import Enum


class ScoreRunSuiteSummaryStatus(str, Enum):
    FAILED = "failed"
    FINISHED = "finished"
    GENERATING = "generating"
    RECORD_CREATED = "record_created"

    def __str__(self) -> str:
        return str(self.value)
