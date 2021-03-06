from typing import Dict, Optional

from mowgli_etl._extractor import _Extractor
from mowgli_etl.pipeline.sentic.sentic_constants import (
    ONTOSENTICNET_OWL_FILENAME,
    SENTIC_FILE_KEY,
)
from mowgli_etl.pipeline.sentic.sentic_constants import ONTOSENTICNET_ZIP_URL
from mowgli_etl.pipeline_storage import PipelineStorage


class SENTICExtractor(_Extractor):
    def __init__(self,sentic_zip_url = ONTOSENTICNET_ZIP_URL, owl_filename=ONTOSENTICNET_OWL_FILENAME,**kwargs ):
        _Extractor.__init__(
            self, **kwargs
        )
        self.__sentic_zip_url = sentic_zip_url
        self.__owl_filename = owl_filename

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
