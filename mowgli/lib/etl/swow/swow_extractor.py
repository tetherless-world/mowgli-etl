<<<<<<< HEAD
from mowgli.lib.etl._extractor import _Extractor

class SwowExtractor(_Extractor):
    def __init__(self, *, csv_file_path: str, **kwds):
        _Extractor.__init__(self)
        self.__csv_file_path = csv_file_path

    def extract(self, **kwds):
        self._logger.info("extract")
        return {"csv_file_path": self.__csv_file_path}
=======
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
>>>>>>> f528e6b5c73c4cc8f9bf8dff32ab4079085d3fde
