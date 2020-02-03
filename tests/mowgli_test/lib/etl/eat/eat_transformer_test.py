from mowgli.lib.etl.eat.eat_transformer import EatTransformer
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
import pathlib
import os

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

    expected_edges = set(Edge(datasource="eat", object_="eat:" + stim_node, relation="cn:RelatedTo", subject="eat:" + response_node) for (stim_node, response_node) in [
        ('SPECIAL', 'TRAIN'),
        ('SPECIAL', 'PARTICULAR'),
        ('SPECIAL', 'EXTRA'),
        ('SPECIAL', 'ORDINARY'),
        ('SPECIAL', 'CASE'),
        ('SPECIAL', 'PERSON'),
        ('SPECIAL', 'BEER'),
        ('SPECIAL', 'CAR'),
        ('SPECIAL', 'CONSTABLE'),
        ('SET', 'TELEVISION'),
        ('SET', 'UP'),
        ('SET', 'OUT'),
        ('SET', 'TO'),
        ('SET', 'DOWN'),
        ('SET', 'GAME'),
        ('SET', 'GROUP'),
        ('SET', 'T.V.'),
        ('SET', 'TEA')
    ])

    assert nodes == expected_nodes
    assert edges == expected_edges