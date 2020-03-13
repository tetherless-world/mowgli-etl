from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.onto.onto_constants import onto_target, STRENGTH_FILE_KEY, onto_archive_path
from typing import Dict, Optional
from io import TextIOWrapper
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.onto.onto_constants import from_url

class ONTOExtractor(_Extractor):
    def __init__(self, from_url=from_url,target=onto_target):
        _Extractor.__init__(self)
        self.__onto_archive_path = onto_archive_path
        self.__from_url = from_url
        self.__target = target

    def extract(self, *, force: bool, storage: PipelineStorage)  -> Optional[Dict[str, object]]: 
        self._download(from_url=self.__from_url, force=force,storage=storage)
        filename = self._extract_zip(force=force,storage=storage,from_url=self.__from_url,target=self.__target)
        return {STRENGTH_FILE_KEY: filename}


