from enum import Enum


class ContentType(str, Enum):
    AUDIO = "audio"
    IMAGE = "image"
    TEXT = "text"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
