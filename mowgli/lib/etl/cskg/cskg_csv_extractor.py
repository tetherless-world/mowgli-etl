from pathlib import Path

from mowgli.lib.etl._extractor import _Extractor


class CskgCsvExtractor(_Extractor):
    def __init__(self, extracted_data_dir_path: Path):
        self.__extracted_data_dir_path = extracted_data_dir_path

    def extract(self, *args, **kwds):
        return {"extracted_data_dir_path": self.__extracted_data_dir_path}
