import hashlib

from rdflib import URIRef, ConjunctiveGraph

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader


class RdfLoader(_Loader):
    def __init__(self, *, pipeline_id: str, format="trig"):
        self.__format = format
        self.__pipeline_id = pipeline_id

    def close(self):
        with open(self.__storage.loaded_data_dir_path / (self.__pipeline_id + "." + self.__format), "w+b") as dest:
            self.__conjunctive_graph.serialize(dest=dest, format=self.__format)

    def load_edge(self, edge):
        # Assumes edges are loaded after the nodes they refer to
        subject_node = self.__nodes_by_id[edge.subject]
        object_node = self.__nodes_by_id[edge.object]

        subject_uri = self.__node_to_uri(subject_node)
        predicate_uri = self.__predicate_to_uri(edge)
        object_uri = self.__node_to_uri(object_node)

        # One context / named graph per edge, so we can reify the edge.
        edge_hash = hashlib.sha256(
            ("%s %s %s" % (edge.subject, edge.predicate, edge.object)).encode("utf-8")).hexdigest()
        context_uri = URIRef("urn:cskg:edge:" + edge_hash)
        context = self.__conjunctive_graph.get_context(context_uri)

        context.add((subject_uri, predicate_uri, object_uri))

    def load_node(self, node):
        assert node.id not in self.__nodes_by_id
        self.__nodes_by_id[node.id] = node

    def open(self, storage):
        self.__conjunctive_graph = ConjunctiveGraph()
        self.__nodes_by_id = {}
        self.__storage = storage
        return self

    def __node_to_uri(self, node: Node) -> URIRef:
        return URIRef("urn:cskg:node:" + node.id)

    def __predicate_to_uri(self, edge: Edge) -> URIRef:
        return URIRef("urn:cskg:edge:" + edge.predicate)
