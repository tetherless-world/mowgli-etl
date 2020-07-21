from csv import DictWriter
from pathlib import Path
from typing import Dict, Callable

from mowgli_etl.loader._edge_loader import _EdgeLoader
from mowgli_etl.loader._node_loader import _NodeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


class CskgCsvNodeLoader(_NodeLoader):
    __NODE_CSV_FIELDS = {
        'aliases': lambda node: ' '.join(node.aliases) if node.aliases is not None else None,
        'other': lambda obj: str(obj.other) if obj.other is not None else None
    }

    def __init__(self, *, bzip: bool = False):
        _NodeLoader.__init__(self)
        self.__bzip = bzip

    def open(self, storage):
        self.__node_file = open(storage.loaded_data_dir_path / "nodes.csv", "w+")
        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__node_writer = DictWriter(self.__node_file, KgNode._fields, **writer_opts)
        self.__node_writer.writeheader()
        return self

    def close(self):
        self.__node_file.close()
        if self.__bzip:
            self._bzip_file(Path(self.__node_file.name))

    def load_node(self, node: KgNode):
        CskgCsvEdgeLoader._write_csv_line(self.__node_writer, self.__NODE_CSV_FIELDS, node)
