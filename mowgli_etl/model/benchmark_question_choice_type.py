from enum import auto,Enum


class BenchmarkQuestionChoiceType(Enum):
    ANSWER = auto()
    HYPOTHESIS = auto()
    SOLUTION = auto()

    @classmethod
    def from_value(cls, value: str):
        val_dict = {
            "BenchmarkAnswer": cls.ANSWER,
            "BenchmarkHypothesis": cls.HYPOTHESIS,
            "BenchmarkSolution": cls.SOLUTION,
        }
        if value not in val_dict:
            raise ValueError(f"Unknown question choice type value {value}")
        return val_dict[value]
