from mowgli_etl.loader.composite_loader import CompositeLoader
from mowgli_etl.loader.json.jsonl_benchmark_answer_loader import (
    JsonlBenchmarkAnswerLoader,
)
from mowgli_etl.loader.json.jsonl_benchmark_loader import JsonlBenchmarkLoader
from mowgli_etl.loader.json.jsonl_benchmark_question_loader import (
    JsonlBenchmarkQuestionLoader,
)
from mowgli_etl.loader.json.jsonl_benchmark_submission_loader import (
    JsonlBenchmarkSubmissionLoader,
)
from mowgli_etl.paths import PROJECT_ROOT
from mowgli_etl.pipeline.mcs_benchmark.mcs_benchmark_pipeline import (
    McsBenchmarkPipeline,
)
from mowgli_etl.pipeline_storage import PipelineStorage


class McsBenchmarkLoader(CompositeLoader):
    def __init__(self, bzip: bool = True):
        CompositeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, *args, **kwds):
        mcs_portal_dir_path = PROJECT_ROOT.parent / "mcs-portal"
        assert (
            mcs_portal_dir_path.is_dir()
        ), f"expected mcs-portal checkout at ${mcs_portal_dir_path}"

        storage = PipelineStorage(
            pipeline_id=McsBenchmarkPipeline.ID,
            root_data_dir_path=PROJECT_ROOT,
            loaded_data_dir_path=mcs_portal_dir_path
            / "app"
            / "benchmark"
            / "conf"
            / "data"
            / "import"
            / "benchmark",
        )
        self._loaders.append(JsonlBenchmarkLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkAnswerLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkQuestionLoader(bzip=self.__bzip).open(storage))
        self._loaders.append(JsonlBenchmarkSubmissionLoader(bzip=self.__bzip).open(storage))
        return self
