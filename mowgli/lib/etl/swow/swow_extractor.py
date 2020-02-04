from io import TextIOWrapper
from typing import Dict, Optional

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._pipeline_storage import _PipelineStorage
from mowgli.lib.etl.swow.swow_constants import STRENGTH_FILE_KEY

class SwowExtractor(_Extractor):
    def __init__(self, swow_archive_path: str):
        _Extractor.__init__(self)
        self.__swow_archive_path = swow_archive_path

    def extract(self, *, force: bool, storage: _PipelineStorage) -> Optional[Dict[str, object]]:
        self._logger.info("extract")
        self._extract_bz2(self.__swow_archive_path, force, storage)
        strength_file_bytes = storage.get(self.__swow_archive_path)
        strength_file_text = TextIOWrapper(strength_file_bytes)
        return {STRENGTH_FILE_KEY: strength_file_text}
