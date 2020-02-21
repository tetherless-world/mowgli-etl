from csv import DictWriter
from io import IOBase
from types import FunctionType
from typing import Dict, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader

class CskgCsvLoader(_Loader):
    def __init__(self, *, node_file: Union[IOBase, str], edge_file: Union[IOBase]):
        self.__edge_file = edge_file
        self.__node_file = node_file

    def __enter__(self):
        if isinstance(self.__edge_file, str):
            self.__edge_file = open(self.__edge_file, "w+")
        if isinstance(self.__node_file, str):
            self.__node_file = open(self.__node_file, "w+")

        edge_fields = self.__class__._edge_csv_fields().keys()
        node_fields = self.__class__._node_csv_fields().keys()

        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__edge_writer = DictWriter(self.__edge_file, edge_fields, **writer_opts)
        self.__node_writer = DictWriter(self.__node_file, node_fields, **writer_opts)

        self.__edge_writer.writeheader()
        self.__node_writer.writeheader()

        return self

    def __exit__(self, *args, **kwds):
        self.__edge_file.close()
        self.__node_file.close()

    @classmethod
    def mime_type(cls):
        return 'csv'

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
