from enum import Enum


class EvalRunExampleInSchemaType(str, Enum):
    FAIL = "fail"
    PASS = "pass"

    def __str__(self) -> str:
        return str(self.value)
