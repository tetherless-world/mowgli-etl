from enum import auto, Enum


class BenchmarkQuestionType(str, Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"

