from pathlib import Path

from mowgli.lib.etl._extractor import _Extractor


class CskgCsvExtractor(_Extractor):
    def __init__(self, *, edges_csv_file_path: Path, nodes_csv_file_path: Path):
        self.__edges_csv_file_path = edges_csv_file_path
        self.__nodes_csv_file_path = nodes_csv_file_path

    def extract(self, *args, **kwds):
        return {
            "edges_csv_file_path": self.__edges_csv_file_path,
            "nodes_csv_file_path": self.__nodes_csv_file_path
        }
