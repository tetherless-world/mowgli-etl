from csv import DictWriter
from typing import Dict, Callable

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader


class CskgCsvLoader(_Loader):
    __EDGE_CSV_FIELDS = {
        'weight': lambda edge: edge.weight if edge.weight is not None else 1.0,
        'other': lambda obj: str(obj.other) if obj.other is not None else None
    }

    __NODE_CSV_FIELDS = {
        'aliases': lambda node: ' '.join(node.aliases) if node.aliases is not None else None,
        'other': lambda obj: str(obj.other) if obj.other is not None else None
    }

    def open(self, storage):
        self.__storage = storage

        # Open in text mode
        self.__edge_file = open(storage.loaded_data_dir_path / "edges.csv", "w+")
        self.__node_file = open(storage.loaded_data_dir_path / "nodes.csv", "w+")

        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__edge_writer = DictWriter(self.__edge_file, Edge._fields, **writer_opts)
        self.__edge_writer.writeheader()

        self.__node_writer = DictWriter(self.__node_file, Node._fields, **writer_opts)
        self.__node_writer.writeheader()

        return self

    def close(self):
        self.__edge_file.close()
        self.__node_file.close()

    def load_edge(self, edge: Edge):
        self._write_csv_line(self.__edge_writer, self.__EDGE_CSV_FIELDS, edge)

    def load_node(self, node: Node):
        self._write_csv_line(self.__node_writer, self.__NODE_CSV_FIELDS, node)

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
