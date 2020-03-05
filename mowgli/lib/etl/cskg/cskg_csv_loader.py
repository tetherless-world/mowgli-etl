from csv import DictWriter
from types import FunctionType
from typing import Dict, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader


class CskgCsvLoader(_Loader):
    def open(self, storage):
        self.__storage = storage

        self.__loaded_node_hashes = set()
        self.__loaded_edge_hashes = set()

        # Open in text mode
        self.__edge_file = open(storage.loaded_data_dir_path / "edges.csv", "w+")
        self.__node_file = open(storage.loaded_data_dir_path / "nodes.csv", "w+")

        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        edge_fields = self.__class__._edge_csv_fields().keys()
        self.__edge_writer = DictWriter(self.__edge_file, edge_fields, **writer_opts)
        self.__edge_writer.writeheader()

        node_fields = self.__class__._node_csv_fields().keys()
        self.__node_writer = DictWriter(self.__node_file, node_fields, **writer_opts)
        self.__node_writer.writeheader()

        return self

    def close(self):
        self.__edge_file.close()
        self.__node_file.close()

    def load_edge(self, edge: Edge):
        edge_hash = hash(edge)
        if edge_hash in self.__loaded_edge_hashes:
            return
        self.__loaded_edge_hashes.add(edge_hash)
        self.__class__._write_csv_line(self.__edge_writer, self.__class__._edge_csv_fields(), edge)

    def load_node(self, node: Node):
        node_hash = hash(node)
        if node_hash in self.__loaded_node_hashes:
            return
        self.__loaded_node_hashes.add(node_hash)
        self.__class__._write_csv_line(self.__node_writer, self.__class__._node_csv_fields(), node)

    # Internal methods

    @classmethod
    def _edge_csv_fields(cls) -> Dict[str, FunctionType]:
        return {
            'subject': Edge.subject.fget,
            'predicate': Edge.predicate.fget,
            'object': Edge.object.fget,
            'datasource': Edge.datasource.fget,
            'weight': cls._serialize_edge_weight,
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

    @staticmethod
    def _serialize_edge_weight(edge: Edge) -> float:
        return edge.weight if edge.weight is not None else 1.0
