from mowgli_etl.model.concept_net_predicates import HAS_A, PART_OF
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.mowgli_predicates import SAME_AS
from mowgli_etl.pipeline.has_part.has_part_extractor import HasPartExtractor
from mowgli_etl.pipeline.has_part.has_part_transformer import HasPartTransformer


def test_has_part_transformer(pipeline_storage):
    extract_result = HasPartExtractor().extract(force=False, storage=pipeline_storage)
    transformer = HasPartTransformer()

    nodes, edges = [], []
    for result in transformer.transform(**extract_result):
        if isinstance(result, KgEdge):
            edges.append(result)

        if len(edges) >= 10:
            break

    assert any(edge for edge in edges if edge.predicate == SAME_AS)
    for edge in edges:
        if edge.predicate == HAS_A:
            assert any(other_edge for other_edge in edges if
                       other_edge.predicate == PART_OF and other_edge.subject == edge.object and other_edge.object == edge.subject)
            break
