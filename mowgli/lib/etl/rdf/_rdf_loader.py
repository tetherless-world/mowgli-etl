from abc import abstractmethod

from rdflib import URIRef

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader


class _RdfLoader(_Loader):
    def __init__(self, *, format: str, pipeline_id: str):
        self.__format = format
        self.__pipeline_id = pipeline_id

    def close(self):
        with open(self.__storage.loaded_data_dir_path / (self.__pipeline_id + "." + self.__format),
                  "w+b") as loaded_file:
            self.__graph.serialize(destination=loaded_file, format=self.__format)

    def load_edge(self, edge):
        # Assumes edges are loaded after the nodes they refer to
        subject_node = self.__nodes_by_id[edge.subject]
        object_node = self.__nodes_by_id[edge.object]
        self._load_edge(edge=edge, graph=self.__graph, object_node=object_node, subject_node=subject_node)

    @abstractmethod
    def _load_edge(self, *, edge: Edge, graph, object_node: Node, subject_node: Node):
        pass

    def load_node(self, node):
        assert node.id not in self.__nodes_by_id
        self.__nodes_by_id[node.id] = node

    @abstractmethod
    def _new_graph(self):
        raise NotImplementedError

    def open(self, storage):
        self.__graph = self._new_graph()
        self.__nodes_by_id = {}
        self.__storage = storage
        return self

    def _node_uri(self, node: Node) -> URIRef:
        return URIRef("urn:cskg:node:" + node.id)

    def _predicate_uri(self, edge: Edge) -> URIRef:
        return URIRef("urn:cskg:predicate:" + edge.predicate)
