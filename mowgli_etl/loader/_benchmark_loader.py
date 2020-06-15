from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_set import BenchmarkQuestionSet
from mowgli_etl.model.edge import Edge


class _BenchmarkLoader(_Loader):
    @abstractmethod
    def load_benchmark(self, benchmark: Benchmark):
        raise NotImplementedError

    @abstractmethod
    def load_benchmark_question(self, benchmark_question: BenchmarkQuestion):
        raise NotImplementedError

    @abstractmethod
    def load_benchmark_question_set(self, benchmark_question_set: BenchmarkQuestionSet):
        raise NotImplementedError
