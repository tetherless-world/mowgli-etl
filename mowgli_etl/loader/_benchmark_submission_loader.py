from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.edge import Edge


class _BenchmarkSubmissionLoader(_Loader):
    @abstractmethod
    def load_benchmark_submission(self, benchmark_submission: BenchmarkSubmission):
        raise NotImplementedError
