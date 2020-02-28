from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import STRENGTH_FILE_KEY
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
from mowgli.lib.etl.swow.swow_transformer import SwowTransformer


def test_transform(sample_swow_strengths_path, sample_swow_edges, sample_swow_nodes):
    transform_args = {STRENGTH_FILE_KEY: sample_swow_strengths_path}
    transformer = SwowTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(**transform_args):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    assert nodes == sample_swow_nodes
    assert edges == sample_swow_edges
