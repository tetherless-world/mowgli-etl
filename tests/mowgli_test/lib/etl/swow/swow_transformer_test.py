from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import SWOW_CSV_FILE_KEY
from mowgli.lib.etl.swow.swow_transformer import SwowTransformer


def test_transform(sample_swow_csv_path, sample_swow_edges, sample_swow_nodes):
    transform_args = {SWOW_CSV_FILE_KEY: sample_swow_csv_path}
    transformer = SwowTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(**transform_args):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    assert nodes == sample_swow_nodes
    assert edges == sample_swow_edges
