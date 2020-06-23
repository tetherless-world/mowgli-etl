from enum import auto, Enum



class BenchmarkQuestionPromptType(Enum):
    GOAL = auto()
    OBSERVATION = auto()
    QUESTION = auto()

    @classmethod
    def from_value(cls, value: str):
        if value not in val_dict:
            raise ValueError(f"Unknown prompt type value {value}")
        return val_dict[value]
