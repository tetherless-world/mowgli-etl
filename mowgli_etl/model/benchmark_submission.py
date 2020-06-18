from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_answer import BenchmarkAnswer


class BenchmarkSubmission(NamedTuple):
    benchmark_id: str
    id: str
    dataset_id: str
    name: str
