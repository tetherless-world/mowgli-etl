from pathlib import Path
from typing import Sequence, Optional

from mowgli_etl._loader import _Loader
from mowgli_etl.loader._benchmark_loader import _BenchmarkLoader
from mowgli_etl.loader._benchmark_question_loader import _BenchmarkQuestionLoader
from mowgli_etl.loader._benchmark_question_set_loader import _BenchmarkQuestionSetLoader
from mowgli_etl.loader._benchmark_submission_loader import _BenchmarkSubmissionLoader
from mowgli_etl.loader._edge_loader import _EdgeLoader
from mowgli_etl.loader._node_loader import _NodeLoader
from mowgli_etl.loader._path_loader import _PathLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_node_loader import CskgCsvNodeLoader
from mowgli_etl.loader.json.json_benchmark_loader import JsonBenchmarkLoader
from mowgli_etl.loader.json.json_benchmark_question_loader import JsonBenchmarkQuestionLoader
from mowgli_etl.loader.json.json_benchmark_question_set_loader import JsonBenchmarkQuestionSetLoader
from mowgli_etl.loader.json.json_benchmark_submission_loader import JsonBenchmarkSubmissionLoader
from mowgli_etl.loader.json.json_edge_loader import JsonEdgeLoader
from mowgli_etl.loader.json.json_node_loader import JsonNodeLoader
from mowgli_etl.loader.json.json_path_loader import JsonPathLoader
from mowgli_etl.loader.json.jsonl_benchmark_loader import JsonlBenchmarkLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_loader import JsonlBenchmarkQuestionLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_set_loader import JsonlBenchmarkQuestionSetLoader
from mowgli_etl.loader.json.jsonl_benchmark_submission_loader import JsonlBenchmarkSubmissionLoader
from mowgli_etl.loader.json.jsonl_path_loader import JsonlPathLoader
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.pipeline_storage import PipelineStorage


class CompositeLoader(_BenchmarkLoader, _BenchmarkQuestionLoader, _BenchmarkQuestionSetLoader, _BenchmarkSubmissionLoader, _EdgeLoader, _NodeLoader, _PathLoader):
    def __init__(self, loaders: Optional[Sequence[_Loader]] = None):
        self._loaders = []
        if loaders is not None:
            self._loaders.extend(loaders)

    def close(self):
        for loader in self._loaders:
            loader.close()

    def load_benchmark(self, benchmark):
        self.__load_model(loader_class=_BenchmarkLoader, load_method_name="load_benchmark", model=benchmark)

    def load_benchmark_question(self, benchmark_question):
        self.__load_model(loader_class=_BenchmarkQuestionLoader, load_method_name="load_benchmark_question", model=benchmark_question)

    def load_benchmark_question_set(self, benchmark_question_set):
        self.__load_model(loader_class=_BenchmarkQuestionSetLoader, load_method_name="load_benchmark_question_set", model=benchmark_question_set)

    def load_benchmark_submission(self, benchmark_submission):
        self.__load_model(loader_class=_BenchmarkSubmissionLoader, load_method_name="load_benchmark_submission", model=benchmark_submission)

    def load_edge(self, edge):
        self.__load_model(loader_class=_EdgeLoader, load_method_name="load_edge", model=edge)

    def __load_model(self, loader_class, load_method_name: str, model) -> None:
        loaded = False
        for loader in self._loaders:
            if not isinstance(loader, loader_class):
                continue
            load_method = getattr(loader, load_method_name)
            load_method(model)
            loaded = True
        if not loaded:
            raise RuntimeError(f"no loader for {model.__class__.__name__}")

    def load_node(self, node):
        self.__load_model(loader_class=_NodeLoader, load_method_name="load_node", model=node)

    def load_path(self, path):
        self.__load_model(loader_class=_PathLoader, load_method_name="load_path", model=path)

    def open(self, storage):
        for loader in self._loaders:
            loader.open(storage)
        return self
