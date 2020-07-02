import pathlib

from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.pipeline.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli_etl.pipeline.sentic.sentic_transformer import SENTICTransformer


def test_transform(sample_sentic_file_path, sample_sentic_nodes, sample_sentic_edges):
    transformer = SENTICTransformer()

    kwdargs = {SENTIC_FILE_KEY: sample_sentic_file_path}
    nodes, edges = set(), set()
    for result in transformer.transform(**kwdargs):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    assert nodes == sample_sentic_nodes
    assert edges == sample_sentic_edges
