from typing import Dict, Optional

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl.pipeline.usf.usf_constants import (
    USF_CUE_TARGET_URL,
    STRENGTH_FILE_KEY,
    USF_CUE_TARGET_FILENAME,
)
from mowgli.lib.etl.pipeline_storage import PipelineStorage


class USFExtractor(_Extractor):
    def __init__(
            self,
        *,
        cue_target_url=USF_CUE_TARGET_URL,
        cue_target_filename=USF_CUE_TARGET_FILENAME,
        **kwargs
    ):
        _Extractor.__init__(self, **kwargs)
        self.__cue_target_url = cue_target_url
        self.__cue_target_filename = cue_target_filename

    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        archive_path = self._download(
            from_url=self.__cue_target_url, force=force, storage=storage
        )
        zip_extraction = self._extract_zip(
            archive_path=archive_path,
            filenames=self.__cue_target_filename,
            force=force,
            storage=storage,
        )
        extracted_file_path = zip_extraction[self.__cue_target_filename]
        return {STRENGTH_FILE_KEY: extracted_file_path}
