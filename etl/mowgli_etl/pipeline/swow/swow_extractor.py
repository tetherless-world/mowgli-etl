from typing import Dict, Optional

from pathvalidate import sanitize_filename

from mowgli_etl.lib.etl._extractor import _Extractor
from mowgli_etl.pipeline.swow.swow_constants import SWOW_CSV_FILE_KEY
from mowgli_etl.pipeline_storage import PipelineStorage


class SwowExtractor(_Extractor):
    def __init__(self, swow_archive_path: str):
        _Extractor.__init__(self)
        self.__swow_archive_path = swow_archive_path

    def extract(self, *, force: bool, storage: PipelineStorage) -> Optional[Dict[str, object]]:
        self._logger.info("extract")
        self._extract_bz2(self.__swow_archive_path, force, storage)
        strength_file_path = storage.extracted_data_dir_path / sanitize_filename(self.__swow_archive_path)
        return {SWOW_CSV_FILE_KEY: strength_file_path}
