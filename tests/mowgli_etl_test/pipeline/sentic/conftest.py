from pathlib import Path

import pytest

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.pipeline.sentic import sentic_types
from mowgli_etl.pipeline.sentic.sentic_mappers import sentic_id, sentic_node, sentic_edge
from tests.mowgli_etl_test.http_client.mock_etl_http_client_test import (
    MockEtlHttpClient,
)

_sample_sentic_file_path = Path(__file__).parent / "test_data.owl"


@pytest.fixture
def strengths():
    return open(_sample_sentic_file_path)


@pytest.fixture
def sample_sentic_nodes():
    expected_sentic_node_names = [
        "pleasantness",
        "attention",
        "sensitivity",
        "aptitude",
        "polarity",
    ]

    expected_concept_node_names = [
        "face",
        "half",
        "swing",
    ]

    expected_primitive_node_names = [
        "joy",
        "admiration",
        "sadness",
        "anger",
    ]

    expected_nodes = set(
        sentic_node(id=name, sentic_type=sentic_types.SENTIC)
        for name in expected_sentic_node_names
    )
    expected_nodes.update(
        set(
            sentic_node(id=name, sentic_type=sentic_types.CONCEPT)
            for name in expected_concept_node_names
        )
    )
    expected_nodes.update(
        set(
            sentic_node(id=name, sentic_type=sentic_types.PRIMITIVE)
            for name in expected_primitive_node_names
        )
    )
    return expected_nodes


@pytest.fixture
def sample_sentic_edges():
    expected_edge_tuples = [
        ("face", "book", None),
        ("face", "time", None),
        ("face", "lift", None),
        ("face", "mask", None),
        ("face", "joy", None),
        ("face", "admiration", None),
        ("face", "pleasantness", 0),
        ("face", "attention", 0.1),
        ("face", "sensitivity", 0.416),
        ("face", "aptitude", -0.80),
        ("face", "polarity", -0.51),
        ("half", "life", None),
        ("half", "whole", None),
        ("half", "part", None),
        ("half", "split", None),
        ("half", "full", None),
        ("half", "sadness", None),
        ("half", "anger", None),
        ("half", "pleasantness", -0.74),
        ("half", "attention", 0),
        ("half", "sensitivity", 0.882),
        ("half", "aptitude", 0.9),
        ("half", "polarity", -0.74),
        ("swing", "bat", None),
        ("swing", "dance", None),
        ("swing", "set", None),
        ("swing", "sway", None),
        ("swing", "joy", None),
        ("swing", "admiration", None),
        ("swing", "pleasantness", -0.04),
        ("swing", "attention", 0.127),
        ("swing", "sensitivity", -0.12),
        ("swing", "aptitude", 0.223),
        ("swing", "polarity", 0.061),
    ]

    expected_edges = set(
        sentic_edge(subject=sentic_id(c), object_=sentic_id(r), weight=w)
        for (c, r, w) in expected_edge_tuples
    )
    return expected_edges


@pytest.fixture
def url():
    return "https://mowgli.com/sentic_test_data.zip"


@pytest.fixture
def senticclient():
    client = MockEtlHttpClient()

    client.add_file_mock_response(
        "https://mowgli.com/sentic_test_data.zip",
        str(Path(__file__).parent / "sentic_test_data.zip"),
    )
    return client
