from rdflib import Graph

from mowgli.lib.etl.rdf._rdf_loader import _RdfLoader


class QuadRdfLoader(_RdfLoader):
    def _load_edge(self, edge, graph, object_node, subject_node):
        object_uri = self._node_uri(object_node)
        predicate_uri = self._predicate_uri(edge)
        subject_uri = self._node_uri(subject_node)

    def _new_graph(self):
        return Graph()
