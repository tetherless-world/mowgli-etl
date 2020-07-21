from csv import DictWriter
from pathlib import Path
from typing import Dict, Callable

from mowgli_etl.loader._kg_edge_loader import _KgEdgeLoader
from mowgli_etl.model.kg_edge import KgEdge


class CskgCsvEdgeLoader(_KgEdgeLoader):
    __EDGE_CSV_FIELDS = {
        'weight': lambda edge: edge.weight if edge.weight is not None else 1.0,
        'other': lambda obj: str(obj.other) if obj.other is not None else None
    }

    def __init__(self, *, bzip: bool = False):
        _KgEdgeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, storage):
        self.__edge_file = open(storage.loaded_data_dir_path / "edges.csv", "w+")
        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__edge_writer = DictWriter(self.__edge_file, KgEdge._fields, **writer_opts)
        self.__edge_writer.writeheader()
        return self

    def close(self):
        self.__edge_file.close()
        if self.__bzip:
            self._bzip_file(Path(self.__edge_file.name))

    def load_kg_edge(self, edge: KgEdge):
        self._write_csv_line(self.__edge_writer, self.__EDGE_CSV_FIELDS, edge)

    # Internal methods
    @staticmethod
    def _write_csv_line(writer: DictWriter, field_dict: Dict[str, Callable[[str], object]], obj):
        """
        Write a line with a writer using serialization methods from the given field_dict
        """

        row_values = {}
        for field in obj._fields:
            serialized = field_dict.get(field, lambda obj: getattr(obj, field))(obj)
            row_values[field] = serialized if serialized is not None else ''
        writer.writerow(row_values)
