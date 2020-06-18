from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_dataset import BenchmarkDataset


class Benchmark(NamedTuple):
    datasets: Tuple[BenchmarkDataset, ...]
    id: str
    name: str
