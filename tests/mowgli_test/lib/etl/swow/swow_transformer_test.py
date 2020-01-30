from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_transformer import SwowTransformer
from mowgli.lib.etl.swow.swow_transformer import SwowTransformer
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
import pathlib
import os

def test_transform():
    test_file_dir = pathlib.Path(__file__).parent.absolute()
    test_file_path = os.path.join(test_file_dir, 'sample_swow_strengths.csv')
    transformer = SwowTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(csv_file_path=test_file_path):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    expected_node_names = ['a', 'one', 'b', 'c', 'indefinite article', 'a few', 'beers', 'bee']
    expected_nodes = set(map(swow_node, expected_node_names))

    expected_edges = set(swow_edge(cue=c, response=r, strength=s) for (c,r,s) in [
        ('a', 'one', 0.118518518518519),
        ('a', 'b', 0.0518518518518519),
        ('a', 'c', 0.0185185185185185),
        ('a', 'indefinite article', 0.00740740740740741),
        ('a few', 'beers', 0.0148698884758364),
        ('b', 'bee', 0.121863799283154),
        ('b', 'c', 0.0896057347670251),
        ('b', 'a', 0.0681003584229391)
    ])

    assert nodes == expected_nodes
    assert edges == expected_edges
