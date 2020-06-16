from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_answer import BenchmarkAnswer


class BenchmarkSubmission(NamedTuple):
    answers: Tuple[BenchmarkAnswer, ...]
    benchmark_id: str
    id: str
    question_set_id: str
