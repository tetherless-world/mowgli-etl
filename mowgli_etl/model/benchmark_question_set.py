from typing import NamedTuple, Tuple


class BenchmarkQuestionSet(NamedTuple):
    benchmark_id: str
    benchmark_question_ids: Tuple[str, ...]
