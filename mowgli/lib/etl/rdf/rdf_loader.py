import hashlib

from rdflib import URIRef, ConjunctiveGraph

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._loader import _Loader


class RdfLoader(_Loader):
    def load_edge(self, edge):
        # Assumes edges are loaded after the nodes they refer to
        subject_node = self.__nodes_by_id[edge.subject]
        object_node = self.__nodes_by_id[edge.object]

        subject_uri = self.__node_to_uri(subject_node)
        predicate_uri = self.__predicate_to_uri(edge)
        object_uri = self.__node_to_uri(object_node)

        edge_hash = hashlib.sha256("%s %s %s" % (edge.subject, edge.predicate, edge.object)).hexdigest()
        context_uri = URIRef("urn:cskg:edge:" + edge_hash)
        context = self.__conjunctive_graph.get_context(context_uri)

        context.add((subject_uri, predicate_uri, object_uri))

    def load_node(self, node):
        assert node.id not in self.__nodes_by_id
        self.__nodes_by_id[node.id] = node

    def open(self, storage):
        self.__conjunctive_graph = ConjunctiveGraph()
        self.__nodes_by_id = {}

    def __node_to_uri(self, node: Node) -> URIRef:
        return URIRef("urn:cskg:node:" + node.id)

    def __predicate_to_uri(self, edge: Edge) -> URIRef:
        return URIRef("urn:cskg:edge:" + edge.predicate)
