from typing import Dict, Optional

from pathvalidate import sanitize_filename

from mowgli_etl._extractor import _extractor
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_CSV_FILE_KEY
from mowgli_etl.pipeline_storage import pipelineStorage

class WdcExtractor(_Extractor):
	def __init__(self, wdc_archive_path: str):
		_Extractor.__init__(self)
		self.__wdc_archive_path = wdc_archive_path

	def extract(self, *, force: bool, storage: PipelineStorage) -> Optional[Dict[str, object]]:
		self._logger.info("extract")
		self._extract_bz2(self.__wdc_archive_path, force, storage)
		strength_file_path = storage.extracted_data_dir_path / sanitize_filename(self.__wdc_archive_path)
		return {WDC_CSV_FILE_KEY: strength_file_path}
