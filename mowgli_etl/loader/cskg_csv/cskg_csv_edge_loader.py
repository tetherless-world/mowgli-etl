from csv import DictWriter
from pathlib import Path
from typing import Dict, Callable

from mowgli_etl.loader._kg_edge_loader import _KgEdgeLoader
from mowgli_etl.model.kg_edge import KgEdge


class CskgCsvEdgeLoader(_KgEdgeLoader):
    __FIELDS = (
        ("subject", lambda edge: edge.subject),
        ("predicate", lambda edge: edge.predicate),
        ("object", lambda edge: edge.object),
        ("datasource", lambda edge: edge.source_ids[0]),
        ("weight", lambda edge: edge.weight if edge.weight is not None else 1.0),
        ("other", lambda edge: None)
    )

    def __init__(self, *, bzip: bool = False):
        _KgEdgeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, storage):
        self.__file = open(storage.loaded_data_dir_path / "edges.csv", "w+")
        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__writer = DictWriter(self.__file, tuple(field[0] for field in self.__FIELDS), **writer_opts)
        self.__writer.writeheader()
        return self

    def close(self):
        self.__file.close()
        if self.__bzip:
            self._bzip_file(Path(self.__file.name))

    def load_kg_edge(self, edge: KgEdge):
        row = {}
        for field in self.__FIELDS:
            value = field[1](edge)
            row[field[0]] = value if value is not None else ''
        self.__writer.writerow(row)
