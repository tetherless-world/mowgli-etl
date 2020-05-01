from pathlib import Path

import pytest

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.sentic.sentic_mappers import sentic_node, sentic_edge
from tests.mowgli_test.lib.etl.http_client.mock_etl_http_client_test import (
    MockEtlHttpClient,
)

_sample_sentic_file_path = Path(__file__).parent / "test_data.owl"


@pytest.fixture
def strengths():
    return open(_sample_sentic_file_path)


@pytest.fixture
def sample_sentic_nodes():
    expected_node_names = [
        "pleasantness",
        "attention",
        "sensitivity",
        "aptitude",
        "polarity",
        "face",
        "book",
        "time",
        "lift",
        "mask",
        "half",
        "life",
        "whole",
        "part",
        "split",
        "full",
        "swing",
        "bat",
        "dance",
        "set",
        "sway",
    ]

    expected_nodes = set(
        sentic_node(name, other={"sentiment": True}) for name in expected_node_names[:5]
    )
    expected_nodes.update(set(sentic_node(name) for name in expected_node_names[5:]))
    return expected_nodes


@pytest.fixture
def sample_sentic_edges():
    expected_edge_tuples = [
        ("face", "book", None, RELATED_TO),
        ("face", "time", None, RELATED_TO),
        ("face", "lift", None, RELATED_TO),
        ("face", "mask", None, RELATED_TO),
        ("face", "pleasantness", 0, RELATED_TO),
        ("face", "attention", 0.1, RELATED_TO),
        ("face", "sensitivity", 0.416, RELATED_TO),
        ("face", "aptitude", -0.80, RELATED_TO),
        ("face", "polarity", -0.51, RELATED_TO),
        ("half", "life", None, RELATED_TO),
        ("half", "whole", None, RELATED_TO),
        ("half", "part", None, RELATED_TO),
        ("half", "split", None, RELATED_TO),
        ("half", "full", None, RELATED_TO),
        ("half", "pleasantness", -0.74, RELATED_TO),
        ("half", "attention", 0, RELATED_TO),
        ("half", "sensitivity", 0.882, RELATED_TO),
        ("half", "aptitude", 0.9, RELATED_TO),
        ("half", "polarity", -0.74, RELATED_TO),
        ("swing", "bat", None, RELATED_TO),
        ("swing", "dance", None, RELATED_TO),
        ("swing", "set", None, RELATED_TO),
        ("swing", "sway", None, RELATED_TO),
        ("swing", "pleasantness", -0.04, RELATED_TO),
        ("swing", "attention", 0.127, RELATED_TO),
        ("swing", "sensitivity", -0.12, RELATED_TO),
        ("swing", "aptitude", 0.223, RELATED_TO),
        ("swing", "polarity", 0.061, RELATED_TO),
    ]

    expected_edges = set(
        sentic_edge(subject=c, object_=r, weight=w, predicate=p)
        for (c, r, w, p) in expected_edge_tuples
    )
    return expected_edges


@pytest.fixture
def url():
    return "https://mowgli.com/sentic_test_data.zip"


@pytest.fixture
def senticclient():
    client = MockEtlHttpClient()

    client.add_file_mock_response(
        "https://mowgli.com/sentic_test_data.zip", str(Path(__file__).parent / "sentic_test_data.zip")
    )
    return client
