from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from typing import Dict, Optional
from mowgli.lib.etl.usf.usf_constants import from_url, STRENGTH_FILE_KEY, usf_target
from io import TextIOWrapper

class USFExtractor(_Extractor):
    def __init__(self):
        _Extractor.__init__(self)

    def extract(self, *, force: bool, storage: PipelineStorage, url=from_url, target=usf_target)  -> Optional[Dict[str, object]]:
        self._download(from_url=url, force=force,storage=storage)
        extracted_file_path = self._extract_zip(force=force,storage=storage,from_url=url,target=target)
        return {STRENGTH_FILE_KEY: extracted_file_path}


