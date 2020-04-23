from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from typing import Dict, Optional
from mowgli.lib.etl.usf.usf_constants import from_url, STRENGTH_FILE_KEY, usf_target
from io import TextIOWrapper
from mowgli.lib.etl.http_client.etl_http_client import EtlHttpClient


class USFExtractor(_Extractor):
    def extract(
        self, *, force: bool, storage: PipelineStorage, url=from_url, target=usf_target
    ) -> Optional[Dict[str, object]]:
        archive_path = self._download(from_url=url, force=force, storage=storage)
        zip_extractions = self._extract_zip(
            archive_path=archive_path, filenames=target, force=force, storage=storage
        )
        extracted_file_path = zip_extractions[target]

        return {STRENGTH_FILE_KEY: extracted_file_path}
