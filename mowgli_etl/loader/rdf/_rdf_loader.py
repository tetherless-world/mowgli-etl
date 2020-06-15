import os
import shutil
from abc import abstractmethod
from typing import Union

import rdflib.plugin
import rdflib.store
from rdflib import URIRef

from mowgli_etl.loader._edge_loader import _EdgeLoader
from mowgli_etl.loader._node_loader import _NodeLoader
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl._loader import _Loader
from mowgli_etl.storage.mem_node_set import MemNodeSet

try:
    from mowgli_etl.storage.persistent_node_set import PersistentNodeSet
except ImportError:
    PersistentNodeSet = None


class _RdfLoader(_EdgeLoader, _NodeLoader):
    def __init__(self, *, format: str, pipeline_id: str):
        _Loader.__init__(self)
        self.__format = format
        self.__pipeline_id = pipeline_id

    def close(self):
        with open(self.__storage.loaded_data_dir_path / (self.__pipeline_id + "." + self.__format),
                  "w+b") as loaded_file:
            self.__graph.serialize(destination=loaded_file, format=self.__format)
        if self.__graph_store_dir_path is not None and os.path.isdir(self.__graph_store_dir_path):
            self.__graph.close()
            shutil.rmtree(self.__graph_store_dir_path)
        self.__nodes.close()

    def load_edge(self, edge):
        # Assumes edges are loaded after the nodes they refer to, if they're going to be loaded at all
        subject_node = self.__nodes.get(edge.subject, default=edge.subject)
        object_node = self.__nodes.get(edge.object, default=edge.object)
        self._load_edge(edge=edge, graph=self.__graph, object_node=object_node, subject_node=subject_node)

    @abstractmethod
    def _load_edge(self, *, edge: Edge, graph, object_node: Union[Node, str], subject_node: Union[Node, str]):
        pass

    def load_node(self, node):
        assert node.id not in self.__nodes, node.id
        self.__nodes.add(node)

    @abstractmethod
    def _new_graph(self, store):
        raise NotImplementedError

    def open(self, storage):
        self.__storage = storage

        try:
            import bsddb3
        except ImportError:
            bsddb3 = None
        if bsddb3 is not None:
            self.__graph_store_dir_path = storage.loaded_data_dir_path / "bsddb"
            if os.path.isdir(self.__graph_store_dir_path):
                shutil.rmtree(self.__graph_store_dir_path)
            os.makedirs(self.__graph_store_dir_path)

            rdflib.plugin.get('Sleepycat', rdflib.store.Store)(str(self.__graph_store_dir_path))

            self.__graph = self._new_graph(store="Sleepycat")
            rt = self.__graph.open(str(self.__graph_store_dir_path), create=True)
            assert rt == rdflib.store.VALID_STORE
        else:
            self._logger.warn("bsddb3 module not available, using in-memory rdflib store")
            self.__graph_store_dir_path = None
            self.__graph = self._new_graph(store="default")

        if PersistentNodeSet is not None:
            self.__nodes = PersistentNodeSet.temporary()
        else:
            self.__nodes = MemNodeSet()

        return self

    def _node_uri(self, node: Union[Node, str]) -> URIRef:
        node_id = node.id if isinstance(node, Node) else node
        return URIRef("urn:cskg:node:" + node_id)

    def _predicate_uri(self, edge: Edge) -> URIRef:
        return URIRef("urn:cskg:predicate:" + edge.predicate)
