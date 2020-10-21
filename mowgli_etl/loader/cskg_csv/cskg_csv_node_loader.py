from csv import DictWriter
from pathlib import Path
from typing import Dict, Callable

from mowgli_etl.loader._kg_edge_loader import _KgEdgeLoader
from mowgli_etl.loader._kg_node_loader import _KgNodeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


class CskgCsvNodeLoader(_KgNodeLoader):
    __FIELDS = (
        ("id", lambda node: node.id),
        ("label", lambda node: node.labels[0]),
        (
            "aliases",
            lambda node: " ".join(node.labels[1:]) if len(node.labels) > 1 else None,
        ),
        ("pos", lambda node: node.pos),
        ("datasource", lambda node: node.source_ids[0]),
        ("other", lambda node: None),
    )

    def __init__(self, *, bzip: bool = False):
        _KgNodeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, storage):
        self.__file = open(storage.loaded_data_dir_path / "nodes.csv", "w+")
        writer_opts = {"delimiter": "\t", "lineterminator": "\n"}
        self.__writer = DictWriter(
            self.__file, tuple(field[0] for field in self.__FIELDS), **writer_opts
        )
        self.__writer.writeheader()
        return self

    def close(self):
        self.__file.close()
        if self.__bzip:
            self._bzip_file(Path(self.__file.name))

    def load_kg_node(self, node: KgNode):
        row = {}
        for field in self.__FIELDS:
            value = field[1](node)
            row[field[0]] = value if value is not None else ""
        self.__writer.writerow(row)
