from enum import Enum


class TestType(str, Enum):
    ACCURACY = "accuracy"
    IMAGE_SAFETY = "image_safety"
    JAILBREAK = "jailbreak"
    MULTITURN_SAFETY = "multiturn_safety"
    SAFETY = "safety"

    def __str__(self) -> str:
        return str(self.value)
