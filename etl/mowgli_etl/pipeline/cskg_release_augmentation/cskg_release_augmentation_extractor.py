from pathlib import Path
from typing import Optional, Dict

from mowgli_etl._extractor import _Extractor
from mowgli_etl.pipeline_storage import PipelineStorage


class CskgReleaseAugmentationExtractor(_Extractor):
    def __init__(self, *, cskg_release_zip_file_path: Optional[Path] = None):
        self.__cskg_release_zip_file_path = cskg_release_zip_file_path

    def extract(self, storage: PipelineStorage, **kwds) -> Optional[Dict[str, object]]:
