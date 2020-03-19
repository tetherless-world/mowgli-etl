import hashlib

from rdflib import ConjunctiveGraph, URIRef, Literal
from rdflib.namespace import DCTERMS, XSD

from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.rdf._rdf_loader import _RdfLoader


class QuadRdfLoader(_RdfLoader):
    __NODE_CONTEXT_CONTEXT_URI = URIRef("urn:cskg:nodeContext")
    __EDGE_CONTEXT_CONTEXT_URI = URIRef("urn:cskg:edgeContext")
    __EDGE_WEIGHT_URI = URIRef("urn:cskg:edgeWeight")

    def __datasource_uri(self, datasource: str):
        return URIRef("urn:cskg:datasource:" + datasource)

    def _load_edge(self, edge, graph, object_node, subject_node):
        object_uri = self._node_uri(object_node)
        predicate_uri = self._predicate_uri(edge)
        subject_uri = self._node_uri(subject_node)

        # One context / named graph per edge, so we can reify the edge.
        edge_hash = hashlib.sha256(
            ("%s %s %s" % (edge.subject, edge.predicate, edge.object)).encode("utf-8")).hexdigest()
        edge_context_uri = URIRef("urn:cskg:edge:" + edge_hash)
        edge_context = graph.get_context(edge_context_uri)

        edge_context.add((subject_uri, predicate_uri, object_uri))

        # Add edge reifications to a different named graph
        edge_context_context = graph.get_context(self.__EDGE_CONTEXT_CONTEXT_URI)
        edge_context_context.add((edge_context_uri, DCTERMS.source, self.__datasource_uri(edge.datasource)))
        if edge.weight is not None:
            edge_context_context.add(
                (edge_context_uri, self.__EDGE_WEIGHT_URI, Literal(edge.weight, datatype=XSD.float)))

        # Add node reifications to a different named graph
        node_context_context = graph.get_context(self.__NODE_CONTEXT_CONTEXT_URI)
        if isinstance(object_node, Node):
            node_context_context.add((object_uri, DCTERMS.source, self.__datasource_uri(object_node.datasource)))
        if isinstance(subject_node, Node):
            node_context_context.add((subject_uri, DCTERMS.source, self.__datasource_uri(subject_node.datasource)))

    def _new_graph(self, store):
        return ConjunctiveGraph(store=store)
