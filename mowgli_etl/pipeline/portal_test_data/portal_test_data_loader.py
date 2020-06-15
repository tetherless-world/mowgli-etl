from pathlib import Path

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


class PortalTestDataLoader(_BenchmarkLoader, _BenchmarkQuestionLoader, _BenchmarkQuestionSetLoader, _BenchmarkSubmissionLoader, _EdgeLoader, _NodeLoader, _PathLoader):
    class __CustomPipelineStorage(PipelineStorage):
        LOADED_DATA_DIR_PATH = PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data"
        assert LOADED_DATA_DIR_PATH.exists(), LOADED_DATA_DIR_PATH

        def __init__(self, *, pipeline_id: str, root_data_dir_path: Path):
            PipelineStorage.__init__(
                self,
                pipeline_id=pipeline_id,
                loaded_data_dir_path=self.LOADED_DATA_DIR_PATH,
                root_data_dir_path=root_data_dir_path
            )

    def __init__(self):
        self.__loaders = []

    def close(self):
        for loader in self.__loaders:
            loader.close()

    def load_benchmark(self, benchmark):
        for loader in self.__loaders:
            if isinstance(loader, _BenchmarkLoader):
                loader.load_benchmark(benchmark)

    def load_benchmark_question(self, benchmark_question):
        for loader in self.__loaders:
            if isinstance(loader, _BenchmarkQuestionLoader):
                loader.load_benchmark_question(benchmark_question)

    def load_benchmark_question_set(self, benchmark_question_set):
        for loader in self.__loaders:
            if isinstance(loader, _BenchmarkQuestionSetLoader):
                loader.load_benchmark_question_set(benchmark_question_set)

    def load_benchmark_submission(self, benchmark_submission):
        for loader in self.__loaders:
            if isinstance(loader, _BenchmarkSubmissionLoader):
                loader.load_benchmark_submission(benchmark_submission)

    def load_edge(self, edge):
        for loader in self.__loaders:
            if isinstance(loader, _EdgeLoader):
                loader.load_edge(edge)

    def load_node(self, node):
        for loader in self.__loaders:
            if isinstance(loader, _NodeLoader):
                loader.load_node(node)

    def load_path(self, path):
        for loader in self.__loaders:
            if isinstance(loader, _PathLoader):
                loader.load_path(path)

    def open(self, storage):
        from mowgli_etl.pipeline.portal_test_data.portal_test_data_pipeline import PortalTestDataPipeline

        ts_benchmark_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "test" / "integration" / "cypress" / "fixtures" / "benchmark")
        ts_kg_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "test" / "integration" / "cypress" / "fixtures" / "kg")
        self.__loaders.append(JsonBenchmarkLoader().open(ts_benchmark_storage))
        self.__loaders.append(JsonBenchmarkQuestionLoader().open(ts_benchmark_storage))
        self.__loaders.append(JsonBenchmarkQuestionSetLoader().open(ts_benchmark_storage))
        self.__loaders.append(JsonBenchmarkSubmissionLoader().open(ts_benchmark_storage))
        self.__loaders.append(JsonEdgeLoader().open(ts_kg_storage))
        self.__loaders.append(JsonNodeLoader().open(ts_kg_storage))
        self.__loaders.append(JsonPathLoader().open(ts_kg_storage))

        scala_benchmark_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data" / "benchmark")
        scala_kg_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data" / "kg")
        self.__loaders.append(CskgCsvEdgeLoader(bzip=True).open(scala_kg_storage))
        self.__loaders.append(CskgCsvNodeLoader(bzip=True).open(scala_kg_storage))
        self.__loaders.append(JsonlBenchmarkLoader().open(scala_benchmark_storage))
        self.__loaders.append(JsonlBenchmarkQuestionLoader().open(scala_benchmark_storage))
        self.__loaders.append(JsonlBenchmarkQuestionSetLoader().open(scala_benchmark_storage))
        self.__loaders.append(JsonlBenchmarkSubmissionLoader().open(scala_benchmark_storage))
        self.__loaders.append(JsonlPathLoader().open(scala_kg_storage))

        return self
