from enum import auto, Enum


class BenchmarkQuestionPromptType(str, Enum):
    GOAL = "GOAL"
    OBSERVATION = "OBSERVATION"
    QUESTION = "QUESTION"
