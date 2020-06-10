from mowgli_etl.model.edge import Edge
from mowgli_etl.model.mowgli_predicates import WN_SYNSET
from mowgli_etl.model.node import Node
from mowgli_etl.pipeline.web_child.web_child_transformer import WebChildTransformer


def test_web_child_transform(web_child_transform_args):
    transformer = WebChildTransformer()
    nodes = {}
    wordnet_edges = {}
    part_whole_edges = []
    for node_or_edge in transformer.transform(**web_child_transform_args):
        if isinstance(node_or_edge, Node):
            nodes[node_or_edge.id] = node_or_edge
        elif isinstance(node_or_edge, Edge):
            edge = node_or_edge
            if edge.predicate == WN_SYNSET:
                assert (
                    edge.subject not in wordnet_edges
                ), "nodes should not have multiple wn mappings"
                wordnet_edges[edge.subject] = edge
            else:
                part_whole_edges.append(edge)

    for nid in nodes.keys():
        assert nid in wordnet_edges

    for ph_edge in part_whole_edges:
        assert ph_edge.subject in nodes
        assert ph_edge.object in nodes

    for wn_edge in wordnet_edges.values():
        assert wn_edge.subject in nodes
