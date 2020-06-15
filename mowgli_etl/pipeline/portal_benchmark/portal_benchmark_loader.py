from pathlib import Path

from mowgli_etl.loader.composite_loader import CompositeLoader
from mowgli_etl.loader.json.jsonl_benchmark_loader import JsonlBenchmarkLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_loader import JsonlBenchmarkQuestionLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_set_loader import JsonlBenchmarkQuestionSetLoader
from mowgli_etl.loader.json.jsonl_benchmark_submission_loader import JsonlBenchmarkSubmissionLoader
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.pipeline.portal_benchmark.portal_benchmark_pipeline import PortalBenchmarkPipeline
from mowgli_etl.pipeline_storage import PipelineStorage


class PortalBenchmarkLoader(CompositeLoader):
    def open(self, *args, **kwds):
        storage = PipelineStorage(pipeline_id=PortalBenchmarkPipeline.ID, root_data_dir_path=PROJECT_ROOT, loaded_data_dir_path=PROJECT_ROOT.parent / "mcs-portal" / "data" / "import" / "benchmark")
        self._loaders.append(JsonlBenchmarkLoader().open(storage))
        self._loaders.append(JsonlBenchmarkQuestionLoader().open(storage))
        self._loaders.append(JsonlBenchmarkQuestionSetLoader().open(storage))
        self._loaders.append(JsonlBenchmarkSubmissionLoader().open(storage))
        return self
