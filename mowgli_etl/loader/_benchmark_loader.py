from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.kg_edge import KgEdge


class _BenchmarkLoader(_Loader):
    @abstractmethod
    def load_benchmark(self, benchmark: Benchmark):
        raise NotImplementedError
