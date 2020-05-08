from mowgli_etl.cskg.concept_net_predicates import IS_A
from mowgli_etl.cskg.edge import Edge
from mowgli_etl.pipeline.food_on.food_on_extractor import FoodOnExtractor
from mowgli_etl.pipeline.food_on.food_on_transformer import FoodOnTransformer


def test_food_on_transformer(pipeline_storage):
    extract_result = FoodOnExtractor().extract(force=False, storage=pipeline_storage)
    transformer = FoodOnTransformer()

    edges = []
    nodes_by_id = {}
    for result in transformer.transform(**extract_result):
        if isinstance(result, Edge):
            edges.append(result)
        else:
            assert result.id not in nodes_by_id
            nodes_by_id[result.id] = result
    for edge in edges:
        assert edge.subject in nodes_by_id
        assert edge.object in nodes_by_id
        assert edge.predicate == IS_A
