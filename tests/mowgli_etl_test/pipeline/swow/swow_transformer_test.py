from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.swow.swow_transformer import SwowTransformer


def test_transform(sample_swow_csv_path, sample_swow_edges, sample_swow_nodes):
    transformer = SwowTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(swow_csv_file=sample_swow_csv_path):
        if isinstance(result, KgNode):
            nodes.add(result)
        elif isinstance(result, KgEdge):
            edges.add(result)

    assert nodes == sample_swow_nodes
    assert edges == sample_swow_edges
