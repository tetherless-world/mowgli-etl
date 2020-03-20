from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.sentic.sentic_constants import sentic_target, SENTIC_FILE_KEY, sentic_archive_path
from typing import Dict, Optional
from io import TextIOWrapper
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.sentic.sentic_constants import from_url

class SENTICExtractor(_Extractor):
    def __init__(self, from_url=from_url,target=sentic_target):
        _Extractor.__init__(self)
        self.__sentic_archive_path = sentic_archive_path
        self.__from_url = from_url
        self.__target = target

    def extract(self, *, force: bool, storage: PipelineStorage)  -> Optional[Dict[str, object]]: 
        self._download(from_url=self.__from_url, force=force,storage=storage)
        filename = self._extract_zip(force=force,storage=storage,from_url=self.__from_url,target=self.__target)
        return {SENTIC_FILE_KEY: filename}


