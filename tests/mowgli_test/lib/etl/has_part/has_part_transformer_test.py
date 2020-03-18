from mowgli.lib.cskg.concept_net_predicates import HAS_A, PART_OF
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.mowgli_predicates import SAME_AS
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.has_part.has_part_extractor import HasPartExtractor
from mowgli.lib.etl.has_part.has_part_transformer import HasPartTransformer


def test_has_part_transformer(pipeline_storage):
    extract_result = HasPartExtractor().extract(force=False, storage=pipeline_storage)
    transformer = HasPartTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(**extract_result):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

        if len(edges) >= 10:
            break

    assert any(edge for edge in edges if edge.predicate == SAME_AS)
    for edge in edges:
        if edge.predicate == HAS_A:
            assert any(other_edge for other_edge in edges if
                       other_edge.predicate == PART_OF and other_edge.subject == edge.object and other_edge.object == edge.subject)
            break
