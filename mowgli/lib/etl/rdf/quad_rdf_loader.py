import hashlib

from rdflib import ConjunctiveGraph, URIRef

from mowgli.lib.etl.rdf._rdf_loader import _RdfLoader


class QuadRdfLoader(_RdfLoader):
    def _load_edge(self, edge, graph, object_node, subject_node):
        object_uri = self._node_uri(object_node)
        predicate_uri = self._predicate_uri(edge)
        subject_uri = self._node_uri(subject_node)

        # One context / named graph per edge, so we can reify the edge.
        edge_hash = hashlib.sha256(
            ("%s %s %s" % (edge.subject, edge.predicate, edge.object)).encode("utf-8")).hexdigest()
        context_uri = URIRef("urn:cskg:edge:" + edge_hash)
        context = graph.get_context(context_uri)

        context.add((subject_uri, predicate_uri, object_uri))

    def _new_graph(self):
        return ConjunctiveGraph()
