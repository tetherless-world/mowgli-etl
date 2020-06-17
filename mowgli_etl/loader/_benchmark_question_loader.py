from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.edge import Edge


class _BenchmarkQuestionLoader(_Loader):
    @abstractmethod
    def load_benchmark_question(self, benchmark_question: BenchmarkQuestion):
        raise NotImplementedError
