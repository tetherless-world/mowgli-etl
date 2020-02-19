from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.usf.usf_transformer import USFTransformer
from mowgli.lib.etl.usf.usf_mappers import usf_edge, usf_node
import pathlib
import os
from mowgli.lib.etl.usf.usf_constants import STRENGTH_FILE_KEY

def test_transform():

    transformer = USFTransformer()


    filetext = open('tests/mowgli_test/lib/etl/usf/usf_test_data.xml')
    kwdargs ={STRENGTH_FILE_KEY:filetext}
    nodes, edges = set(), set()
    for result in transformer.transform(**kwdargs):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    expected_node_names = {'face':'N', 'book':'N', 'time':'N', 'lift':'V', 'mask':'N', 'half':'N', 'life':'N', 'whole':'N', 'part':'N','split':'V' ,
                        'full':'AJ', 'swing':'V', 'bat':'N', 'dance':'V', 'set':'N', 'sway':'V'}

    expected_nodes = set( usf_node(name,pos) for name,pos in  expected_node_names.items() )

    expected_edge_tuples = [
        ('face', 'book', 0.429),
        ('face', 'time', 0.286),
        ('face', 'lift', 0.143),
        ('face', 'mask', 0.143),
        ('half', 'life', 0.455),
        ('half', 'whole', 0.182),
        ('half', 'part', 0.182),
        ('half', 'split', 0.091),
        ('half', 'full', 0.091),
        ('swing', 'bat', 0.4),
        ('swing', 'dance', 0.2),
        ('swing', 'set', 0.2),
        ('swing', 'sway', 0.2)    
    ]

    expected_edges = set(usf_edge(cue=c, response=r, strength=s) for (c,r,s) in expected_edge_tuples)

    assert nodes == expected_nodes
    assert edges == expected_edges