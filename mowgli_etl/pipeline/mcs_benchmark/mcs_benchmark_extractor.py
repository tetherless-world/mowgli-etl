from typing import Dict, Optional

from mowgli_etl._extractor import _Extractor
from mowgli_etl.paths import DATA_DIR
from mowgli_etl.pipeline_storage import PipelineStorage


class McsBenchmarkExtractor(_Extractor):
    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        return {
            "benchmark_sample_path": DATA_DIR
            / "mcs_benchmark"
            / "extracted"
            / "PhysicalIQA_dev.jsonl"
        }
