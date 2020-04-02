from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.usf.usf_transformer import USFTransformer
from mowgli.lib.etl.usf.usf_mappers import usf_edge, usf_node
import pathlib
import os
from mowgli.lib.etl.usf.usf_constants import STRENGTH_FILE_KEY


def test_transform():
    transformer = USFTransformer()

    file_path = pathlib.Path(__file__).parent / 'usf_test_data.xml'
    kwdargs = {STRENGTH_FILE_KEY: file_path}
    nodes, edges = set(), set()
    for result in transformer.transform(**kwdargs):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    expected_node_names = {'face': [9999,'N'], 'book': [117,'N',3.23], 'time':[426,'N',1.17] , 
                            'lift': [5,'V',4.00], 'mask': [24,'N',0.45], 'half': [23,'N'],
                            'life': [234,'N',2.11], 'whole': [92,'N',4.12], 'part': [33, 'N',0.82],
                            'split': [104,'V',0.2],'full': [720,'AJ',5.5], 'swing': [36,'V'], 
                            'bat': [230,'N',1.76], 'dance': [321,'V',1.62], 'set': [620,'N',7.00], 
                            'sway': [923,'V',0.84]}

    expected_nodes = set(usf_node(cueOrResponse=name,pos=attlist[1],other={'fr':attlist[0]})
                        if len(attlist) == 2 else
                        usf_node(cueOrResponse=name,pos=attlist[1],other={'fr':attlist[0],'con':attlist[2]} )
                        for name, attlist in expected_node_names.items())

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

    expected_edges = set(usf_edge(cue=c, response=r, strength=s) for (c, r, s) in expected_edge_tuples)

    assert nodes == expected_nodes
    assert edges == expected_edges
