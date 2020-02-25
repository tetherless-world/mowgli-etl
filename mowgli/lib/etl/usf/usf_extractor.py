from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._pipeline_storage import _PipelineStorage
from typing import Dict, Optional
from mowgli.lib.etl.usf.usf_constants import from_url, STRENGTH_FILE_KEY, usf_target
from io import TextIOWrapper

class USFExtractor(_Extractor):
    def __init__(self):
        _Extractor.__init__(self)
    
    def extract(self, *, force: bool, storage: _PipelineStorage, url=from_url, target=usf_target)  -> Optional[Dict[str, object]]:
        self._download(from_url=url, force=force,storage=storage)
        filename = self._extract_zip(force=force,storage=storage,from_url=url,target=target)
        strength_file_bytes = storage.get(filename)
        strength_file_text = TextIOWrapper(strength_file_bytes)
        return {STRENGTH_FILE_KEY: strength_file_text}


      