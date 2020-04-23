from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.sentic.sentic_constants import (
    ONTOSENTICNET_OWL_FILENAME,
    SENTIC_FILE_KEY,
    SENTIC_ARCHIVE_PATH,
)
from typing import Dict, Optional
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL


class SENTICExtractor(_Extractor):
    def __init__(
        self, *, from_url=ONTOSENTICNET_ZIP_URL, target=ONTOSENTICNET_OWL_FILENAME
    ):
        _Extractor.__init__(self)
        self.__sentic_archive_path = SENTIC_ARCHIVE_PATH
        self.__from_url = from_url
        self.__target = target

    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        archive_path = self._download(
            from_url=self.__from_url, force=force, storage=storage
        )
        zip_extractions = self._extract_zip(
            archive_path=archive_path,
            filenames=self.__target,
            force=force,
            storage=storage,
        )
        filename = zip_extractions[self.__target]
        return {SENTIC_FILE_KEY: filename}
