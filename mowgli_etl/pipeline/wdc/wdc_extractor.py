from typing import Dict, Optional

from pathvalidate import sanitize_filename

from mowgli_etl._extractor import _Extractor
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_CSV_FILE_KEY
from mowgli_etl.pipeline_storage import PipelineStorage
from mowgli_etl.paths import DATA_DIR

class WdcExtractor(_Extractor):
    _WDC_ARCHIVE_PATH = DATA_DIR / "wdc" / "extracted" / "offers_corpus_english_v2_random_100.jsonl"

    def extract(self, *, force: bool, storage: PipelineStorage) -> Optional[Dict[str, object]]:
        self._logger.info("extract")
        self._extract_bz2(_WDC_ARCHIVE_PATH, force, storage)
        strength_file_path = storage.extracted_data_dir_path / sanitize_filename(_WDC_ARCHIVE_PATH)
        return {WDC_CSV_FILE_KEY: strength_file_path}
