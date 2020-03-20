from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
import pathlib
import os
from mowgli.lib.etl.onto.onto_mappers import onto_node, onto_edge
from mowgli.lib.etl.onto.onto_constants import ONTOLOGY_FILE_KEY
from mowgli.lib.etl.onto.onto_transformer import ONTOTransformer

def test_transform(sample_onto_nodes, sample_onto_edges):
    transformer = ONTOTransformer()


    filepath = pathlib.Path(__file__).parent / 'test_data.owl'
    kwdargs ={ONTOLOGY_FILE_KEY:filepath}
    nodes, edges = set(), set()
    for result in transformer.transform(**kwdargs):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)


    assert nodes == sample_onto_nodes
    assert edges == sample_onto_edges