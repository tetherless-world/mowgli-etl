from pathlib import Path

from configargparse import ArgParser

from mowgli_etl.lib.etl._extractor import _Extractor


class CskgCsvExtractor(_Extractor):
    def __init__(self, *, edges_csv_file_paths, nodes_csv_file_paths):
        self.__edges_csv_file_paths = tuple(
            path if isinstance(path, Path) else Path(path) for path in edges_csv_file_paths)
        self.__nodes_csv_file_paths = tuple(
            path if isinstance(path, Path) else Path(path) for path in nodes_csv_file_paths)

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser):
        arg_parser.add_argument("--edges-csv-file-path", dest="edges_csv_file_paths", action="append", required=True)
        arg_parser.add_argument("--nodes-csv-file-path", dest="nodes_csv_file_paths", action="append", required=True)

    def extract(self, *args, **kwds):
        return {
            "edges_csv_file_paths": self.__edges_csv_file_paths,
            "nodes_csv_file_paths": self.__nodes_csv_file_paths
        }
