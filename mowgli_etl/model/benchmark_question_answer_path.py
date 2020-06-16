from typing import NamedTuple, Tuple


class BenchmarkQuestionAnswerPath(NamedTuple):
    path: Tuple[str, ...]
    score: float
