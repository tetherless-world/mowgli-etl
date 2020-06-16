from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_question_set import BenchmarkQuestionSet


class Benchmark(NamedTuple):
    id: str
    name: str
    question_sets: Tuple[BenchmarkQuestionSet, ...]
