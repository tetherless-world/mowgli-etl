import os
import pathlib

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.pipeline.eat.eat_transformer import EatTransformer


def test_eat_tranform():
    test_file_dir = pathlib.Path(__file__).parent.absolute()
    test_file_path = os.path.join(test_file_dir, 'sample_eat100.xml')
    transformer = EatTransformer()

    nodes, edges = set(), set()
    for result in transformer.transform(xml_file_path=test_file_path):
        if isinstance(result, Node):
            nodes.add(result)
        elif isinstance(result, Edge):
            edges.add(result)

    expected_stimulus_nodes = set(Node(datasource="eat", id="eat:" + stim_word, label=stim_word) for stim_word in [
        'SPECIAL',
        'SET'
    ])

    expected_response_nodes = set(Node(datasource="eat", id="eat:" + response_word, label=response_word) for response_word in [
        'TRAIN',
        'PARTICULAR',
        'EXTRA',
        'ORDINARY',
        'CASE',
        'PERSON',
        'BEER',
        'CAR',
        'CONSTABLE',
        'TELEVISION',
        'UP',
        'OUT',
        'TO',
        'DOWN',
        'GAME',
        'GROUP',
        'T.V.',
        'TEA'
    ])

    expected_nodes = expected_stimulus_nodes | expected_response_nodes

    expected_edges = set(
        Edge(datasource="eat", object="eat:" + stim_node, predicate="cn:RelatedTo", subject="eat:" + response_node,
             weight=response_weight) for (stim_node, response_node, response_weight) in [
            ('SPECIAL', 'TRAIN', 0.07),
            ('SPECIAL', 'PARTICULAR', 0.05),
            ('SPECIAL', 'EXTRA', 0.04),
            ('SPECIAL', 'ORDINARY', 0.04),
            ('SPECIAL', 'CASE', 0.03),
            ('SPECIAL', 'PERSON', 0.03),
            ('SPECIAL', 'BEER', 0.02),
            ('SPECIAL', 'CAR', 0.02),
            ('SPECIAL', 'CONSTABLE', 0.02),
            ('SET', 'TELEVISION', 0.06),
        ('SET', 'UP', 0.05),
        ('SET', 'OUT', 0.04),
        ('SET', 'TO', 0.04),
        ('SET', 'DOWN', 0.03),
        ('SET', 'GAME', 0.03),
        ('SET', 'GROUP', 0.03),
        ('SET', 'T.V.', 0.03),
        ('SET', 'TEA', 0.03)
    ])

    assert nodes == expected_nodes
    assert edges == expected_edges
