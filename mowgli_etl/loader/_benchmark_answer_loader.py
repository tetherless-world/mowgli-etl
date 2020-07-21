from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.kg_edge import KgEdge


class _BenchmarkAnswerLoader(_Loader):
    @abstractmethod
    def load_benchmark_answer(self, benchmark_answer: BenchmarkAnswer):
        raise NotImplementedError
