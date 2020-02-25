from io import TextIOWrapper
from typing import Dict, Optional

from pathvalidate import sanitize_filename

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.swow.swow_constants import STRENGTH_FILE_KEY

class SwowExtractor(_Extractor):
    def __init__(self, swow_archive_path: str):
        _Extractor.__init__(self)
        self.__swow_archive_path = swow_archive_path

    def extract(self, *, force: bool, storage: PipelineStorage) -> Optional[Dict[str, object]]:
        self._logger.info("extract")
        self._extract_bz2(self.__swow_archive_path, force, storage)
        with open(storage.extracted_data_dir_path / sanitize_filename(self.__swow_archive_path), "r") as f:
            strength_file_text = f.read()
        return {STRENGTH_FILE_KEY: strength_file_text}
