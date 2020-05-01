from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.pipeline.swow.swow_transformer import SwowTransformer


def test_transform(sample_swow_csv_path, sample_swow_edges, sample_swow_nodes):
    transformer = SwowTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(swow_csv_file=sample_swow_csv_path):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    assert nodes == sample_swow_nodes
    assert edges == sample_swow_edges
