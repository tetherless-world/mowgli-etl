from mowgli_etl.loader.composite_loader import CompositeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_node_loader import CskgCsvNodeLoader
from mowgli_etl.loader.json.json_benchmark_answer_loader import JsonBenchmarkAnswerLoader
from mowgli_etl.loader.json.json_benchmark_loader import JsonBenchmarkLoader
from mowgli_etl.loader.json.json_benchmark_question_loader import JsonBenchmarkQuestionLoader
from mowgli_etl.loader.json.json_benchmark_submission_loader import JsonBenchmarkSubmissionLoader
from mowgli_etl.loader.json.json_edge_loader import JsonEdgeLoader
from mowgli_etl.loader.json.json_node_loader import JsonNodeLoader
from mowgli_etl.loader.json.json_path_loader import JsonPathLoader
from mowgli_etl.loader.json.jsonl_benchmark_answer_loader import JsonlBenchmarkAnswerLoader
from mowgli_etl.loader.json.jsonl_benchmark_loader import JsonlBenchmarkLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_loader import JsonlBenchmarkQuestionLoader
from mowgli_etl.loader.json.jsonl_benchmark_submission_loader import JsonlBenchmarkSubmissionLoader
from mowgli_etl.loader.json.jsonl_path_loader import JsonlPathLoader
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.pipeline_storage import PipelineStorage


class PortalTestDataLoader(CompositeLoader):
    def open(self, storage):
        from mowgli_etl.pipeline.portal_test_data.portal_test_data_pipeline import PortalTestDataPipeline

        ts_benchmark_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "test" / "integration" / "cypress" / "fixtures" / "benchmark")
        ts_kg_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "test" / "integration" / "cypress" / "fixtures" / "kg")
        self._loaders.append(JsonBenchmarkLoader().open(ts_benchmark_storage))
        self._loaders.append(JsonBenchmarkAnswerLoader().open(ts_benchmark_storage))
        self._loaders.append(JsonBenchmarkQuestionLoader().open(ts_benchmark_storage))
        self._loaders.append(JsonBenchmarkSubmissionLoader().open(ts_benchmark_storage))
        self._loaders.append(JsonEdgeLoader().open(ts_kg_storage))
        self._loaders.append(JsonNodeLoader().open(ts_kg_storage))
        self._loaders.append(JsonPathLoader().open(ts_kg_storage))

        scala_benchmark_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data" / "benchmark")
        scala_kg_storage = PipelineStorage(pipeline_id=PortalTestDataPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "conf" / "test_data" / "kg")
        self._loaders.append(CskgCsvEdgeLoader(bzip=True).open(scala_kg_storage))
        self._loaders.append(CskgCsvNodeLoader(bzip=True).open(scala_kg_storage))
        self._loaders.append(JsonlBenchmarkAnswerLoader().open(scala_benchmark_storage))
        self._loaders.append(JsonlBenchmarkLoader().open(scala_benchmark_storage))
        self._loaders.append(JsonlBenchmarkQuestionLoader().open(scala_benchmark_storage))
        self._loaders.append(JsonlBenchmarkSubmissionLoader().open(scala_benchmark_storage))
        self._loaders.append(JsonlPathLoader().open(scala_kg_storage))

        return self
