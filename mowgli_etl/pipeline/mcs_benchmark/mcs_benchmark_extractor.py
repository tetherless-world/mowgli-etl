from typing import Dict, Optional

from mowgli_etl._extractor import _Extractor
from mowgli_etl.paths import DATA_DIR, PROJECT_ROOT
from mowgli_etl.pipeline_storage import PipelineStorage


class McsBenchmarkExtractor(_Extractor):
    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        jsonl_paths = []
        benchmark_project_path = PROJECT_ROOT.parent / "CommonsenseBenchmark"
        if benchmark_project_path.exists():
            for benchmark_path in (benchmark_project_path / "converted").iterdir():
                for benchmark_jsonl_path in benchmark_path.glob("*.jsonl"):
                    jsonl_paths.append(benchmark_jsonl_path)
        assert (
            len(jsonl_paths) > 0
        ), f"No benchmark jsonl files found in {benchmark_project_path}"
        return {"benchmark_jsonl_paths": tuple(jsonl_paths)}
