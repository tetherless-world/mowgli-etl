from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.sentic.sentic_constants import (
    sentic_target,
    SENTIC_FILE_KEY,
    sentic_archive_path,
    ONTOSENTICNET_OWL_FILENAME,
    SENTIC_FILE_KEY,
)
from typing import Dict, Optional
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL



class SENTICExtractor(_Extractor):
    def __init__(self, **kwargs):
        _Extractor.__init__(
            self, kwargs.get("http_client") if kwargs.get("http_client") else None
        )
        self.__sentic_zip_url = kwargs.get("sentic_zip_url") if kwargs.get("sentic_zip_url") else ONTOSENTICNET_ZIP_URL
        self.__owl_filename = kwargs.get("owl_filename") if kwargs.get("owl_filename") else ONTOSENTICNET_OWL_FILENAME

    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        archive_path = self._download(
            from_url=self.__sentic_zip_url, force=force, storage=storage
        )
        zip_extractions = self._extract_zip(
            archive_path=archive_path,
            filenames=self.__owl_filename,
            force=force,
            storage=storage,
        )
        filename = zip_extractions[self.__owl_filename]
        return {SENTIC_FILE_KEY: filename}
