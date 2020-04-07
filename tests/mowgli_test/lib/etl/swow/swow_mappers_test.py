from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import SWOW_DATASOURCE_ID, SWOW_NAMESPACE
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node, SwowResponseCounter


def test_swow_node():
    node = swow_node(
        word="test response", response_counts=SwowResponseCounter(r1=3, r2=2, r3=0)
    )
    expected_node = Node(
        datasource=SWOW_DATASOURCE_ID,
        id=f'{SWOW_NAMESPACE}:{quote("test response")}',
        label="test response",
        other={"response_counts": {"R1": 3, "R2": 2, "R3": 0}},
    )
    assert node == expected_node


def test_swow_edge():
    edge = swow_edge(
        cue="test",
        response="test response",
        cue_response_counts=SwowResponseCounter(r1=2, r3=4),
        response_counts=SwowResponseCounter(r1=1, r3=1),
    )
    expected_edge = Edge(
        datasource=SWOW_DATASOURCE_ID,
        subject=f"{SWOW_NAMESPACE}:test",
        object_=f'{SWOW_NAMESPACE}:{quote("test response")}',
        predicate=RELATED_TO,
        weight=2 / 6,
        other={
            "response_counts": {"R1": 1, "R2": 0, "R3": 1},
            "response_strengths": {"R1": 1 / 2, "R2": 0, "R3": 1 / 4},
        },
    )
    assert edge == expected_edge


def test_swow_resp_counter_default():
    counter = SwowResponseCounter(r2=4)
    expected_counts = {"R1": 0, "R2": 4, "R3": 0}
    assert counter.counts == expected_counts


def test_swow_resp_counter_increments():
    counter = SwowResponseCounter()
    for _ in range(3):
        counter.increment_resp_count("R1")
    for _ in range(7):
        counter.increment_resp_count("R3")
    expected_counts = {"R1": 3, "R2": 0, "R3": 7}
    assert counter.counts == expected_counts
