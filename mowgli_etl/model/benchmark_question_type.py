from enum import auto, Enum


class BenchmarkQuestionType(Enum):
    MULTIPLE_CHOICE = auto()
    TRUE_FALSE = auto()

    @classmethod
    def from_value(cls, value: str):
        if value not in val_dict:
            raise ValueError(f"Unknown question type value {value}")
        return val_dict[value]
