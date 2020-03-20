from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
import pathlib
import os
from mowgli.lib.etl.sentic.sentic_mappers import sentic_node, sentic_edge
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_FILE_KEY
from mowgli.lib.etl.sentic.sentic_transformer import SENTICTransformer

def test_transform(sample_sentic_nodes, sample_sentic_edges):
    transformer = SENTICTransformer()


    filepath = pathlib.Path(__file__).parent / 'test_data.owl'
    kwdargs ={SENTIC_FILE_KEY:filepath}
    nodes, edges = set(), set()
    for result in transformer.transform(**kwdargs):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)


    assert nodes == sample_sentic_nodes
    assert edges == sample_sentic_edges