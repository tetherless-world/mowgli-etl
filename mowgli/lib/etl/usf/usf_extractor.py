from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._pipeline_storage import _PipelineStorage
from typing import Dict, Optional
from mowgli.lib.etl.usf.usf_constants import from_url, STRENGTH_FILE_KEY
from io import TextIOWrapper

class USFExtractor(_Extractor):
    def __init__(self):
        _Extractor.__init__(self)
    
    def extract(self, *, force: bool, storage: _PipelineStorage, url=from_url)  -> Optional[Dict[str, object]]:
        filename = self._extract_zip(force=force,storage=storage,from_url=url)
        strength_file_bytes = storage.get(filename)
        strength_file_text = TextIOWrapper(strength_file_bytes)
        return {STRENGTH_FILE_KEY: strength_file_text}


      