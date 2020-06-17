from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_dataset import BenchmarkDataset


class Benchmark(NamedTuple):
    id: str
    name: str
    datasets: Tuple[BenchmarkDataset, ...]
