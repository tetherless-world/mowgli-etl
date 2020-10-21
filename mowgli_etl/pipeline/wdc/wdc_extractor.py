from typing import Dict, Optional

from pathvalidate import sanitize_filename

from mowgli_etl._extractor import _Extractor
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_CSV_FILE_KEY, WDC_ARCHIVE_PATH
from mowgli_etl.pipeline_storage import PipelineStorage
from mowgli_etl.paths import DATA_DIR


class WdcExtractor(_Extractor):
    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        return {
            WDC_CSV_FILE_KEY: WDC_ARCHIVE_PATH
            / "offers_corpus_english_v2_random_100.jsonl"
        }
