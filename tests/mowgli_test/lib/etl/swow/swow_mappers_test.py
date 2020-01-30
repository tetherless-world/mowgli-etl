from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge

def test_swow_node():
    node = swow_node('test response')
    expected_node = Node(
        datasource='swow',
        id='swow:test_response',
        label='test response'
    )
    assert node == expected_node

def test_swow_edge():
    edge = swow_edge(
        cue='test',
        response='test response',
        strength=0.3
    )
    expected_edge = Edge(
        datasource='swow',
        subject='swow:test',
        object_='swow:test_response',
        relation='/r/RelatedTo',
        weight=0.3
    )
    assert edge == expected_edge
