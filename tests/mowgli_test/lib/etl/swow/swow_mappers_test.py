from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import SWOW_DATASOURCE_ID, SWOW_NAMESPACE
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node


def test_swow_node():
    node = swow_node('test response')
    expected_node = Node(
        datasource=SWOW_DATASOURCE_ID,
        id=f'{SWOW_NAMESPACE}:{quote("test_response")}',
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
        datasource=SWOW_DATASOURCE_ID,
        subject=f'{SWOW_NAMESPACE}:test',
        object_=f'{SWOW_NAMESPACE}:{quote("test_response")}',
        predicate=RELATED_TO,
        weight=0.3
    )
    assert edge == expected_edge
