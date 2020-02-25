from csv import DictWriter
from io import StringIO
from types import FunctionType
from typing import Dict, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader

class CskgCsvLoader(_Loader):
    def open(self, storage):
        self.__storage = storage

        self.__edge_file = StringIO()
        self.__node_file = StringIO()

        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        edge_fields = self.__class__._edge_csv_fields().keys()
        self.__edge_writer = DictWriter(self.__edge_file, edge_fields, **writer_opts)
        self.__edge_writer.writeheader()

        node_fields = self.__class__._node_csv_fields().keys()
        self.__node_writer = DictWriter(self.__node_file, node_fields, **writer_opts)
        self.__node_writer.writeheader()

        return self

    def close(self):
        self.__storage.put("edges.csv", self.__edge_file.getvalue())
        self.__storage.put("nodes.csv", self.__node_file.getvalue())

    def load_edge(self, edge: Edge):
        self.__class__._write_csv_line(self.__edge_writer, self.__class__._edge_csv_fields(), edge)

    def load_node(self, node: Node):
        self.__class__._write_csv_line(self.__node_writer, self.__class__._node_csv_fields(), node)

    # Internal methods

    @classmethod
    def _edge_csv_fields(cls) -> Dict[str, FunctionType]:
        return {
            'subject': Edge.subject.fget,
            'predicate': Edge.relation.fget,
            'object': Edge.object.fget,
            'datasource': Edge.datasource.fget,
            'weight': Edge.weight.fget,
            'other': cls._serialize_other
        }

    @classmethod
    def _node_csv_fields(cls) -> Dict[str, FunctionType]:
        return {
            'id': Node.id.fget,
            'label': Node.label.fget,
            'aliases': cls._serialize_node_aliases,
            'pos': Node.pos.fget,
            'datasource': Node.datasource.fget,
            'other': cls._serialize_other
        }

    @staticmethod
    def _write_csv_line(writer: DictWriter, field_dict: Dict[str, FunctionType], obj):
        """
        Write a line with a writer using serialization methods from the given field_dict
        """
        row_values = {field: serialize_field(obj) for field, serialize_field in field_dict.items()}
        writer.writerow(row_values)

    @staticmethod
    def _serialize_field(value, serialize_fn: FunctionType) -> str:
        """
        Call serialization function on a value and handle None values
        """
        serialized = serialize_fn(value)
        return serialized if serialized is not None else ''

    @staticmethod
    def _serialize_other(obj: Union[Edge, Node]) -> str:
        return str(obj.other) if obj.other is not None else None

    @staticmethod
    def _serialize_node_aliases(node: Node) -> str:
        return ' '.join(node.aliases) if node.aliases is not None else None