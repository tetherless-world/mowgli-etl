from enum import auto,Enum


class BenchmarkQuestionChoiceType(str, Enum):
    ANSWER = "ANSWER"
    HYPOTHESIS = "HYPOTHESIS"
    SOLUTION = "SOLUTION"
