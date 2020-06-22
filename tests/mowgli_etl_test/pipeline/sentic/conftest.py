import zipfile
from pathlib import Path

import pytest

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.pipeline.sentic import sentic_types
from mowgli_etl.pipeline.sentic.sentic_mappers import (
    sentic_id,
    sentic_node,
    sentic_edge,
)
from mowgli_etl.pipeline.sentic.sentic_types import CONCEPT, PRIMITIVE, SENTIC
from tests.mowgli_etl_test.http_client.mock_etl_http_client_test import (
    MockEtlHttpClient,
)


@pytest.fixture
def sample_sentic_file_path() -> Path:
    return Path(__file__).parent / "test_data.owl"


@pytest.fixture
def sample_sentic_zip_client(
    tmp_path_factory,
    sample_sentic_file_path,
    sentic_zip_url,
    sample_sentic_zip_owl_filename,
) -> MockEtlHttpClient:
    zip_path = tmp_path_factory.mktemp("sentic-test") / "sentic_test_data.zip"
    zipfile.ZipFile(zip_path, mode="w").write(sample_sentic_file_path, arcname=sample_sentic_file_path.name)
    client = MockEtlHttpClient()
    client.add_file_mock_response(
        sentic_zip_url, zip_path
    )
    return client


@pytest.fixture
def sample_sentic_zip_owl_filename(sample_sentic_file_path) -> str:
    return sample_sentic_file_path.name

@pytest.fixture
def full_sentic_zip_path() -> Path:
    return Path(__file__).parent / "ontosenticnet.zip"

@pytest.fixture
def full_sentic_zip_owl_filename() -> str:
    return "ontosenticnet/ontosenticnet.owl"

@pytest.fixture
def full_sentic_zip_client(
        tmp_path_factory,
        full_sentic_zip_path,
        sentic_zip_url,
) -> MockEtlHttpClient:
    client = MockEtlHttpClient()
    client.add_file_mock_response(
        sentic_zip_url, full_sentic_zip_path
    )
    return client

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
        ("face", "book", CONCEPT, None),
        ("face", "time", CONCEPT, None),
        ("face", "lift", CONCEPT, None),
        ("face", "mask", CONCEPT, None),
        ("face", "joy", PRIMITIVE, None),
        ("face", "admiration", PRIMITIVE, None),
        ("face", "pleasantness", SENTIC, 0),
        ("face", "attention", SENTIC, 0.1),
        ("face", "sensitivity", SENTIC, 0.416),
        ("face", "aptitude", SENTIC, -0.80),
        ("face", "polarity", SENTIC, -0.51),
        ("half", "life", CONCEPT, None),
        ("half", "whole", CONCEPT, None),
        ("half", "part", CONCEPT, None),
        ("half", "split", CONCEPT, None),
        ("half", "full", CONCEPT, None),
        ("half", "sadness", PRIMITIVE, None),
        ("half", "anger", PRIMITIVE, None),
        ("half", "pleasantness", SENTIC, -0.74),
        ("half", "attention", SENTIC, 0),
        ("half", "sensitivity", SENTIC, 0.882),
        ("half", "aptitude", SENTIC, 0.9),
        ("half", "polarity", SENTIC, -0.74),
        ("swing", "bat", CONCEPT, None),
        ("swing", "dance", CONCEPT, None),
        ("swing", "set", CONCEPT, None),
        ("swing", "sway", CONCEPT, None),
        ("swing", "joy", PRIMITIVE, None),
        ("swing", "admiration", PRIMITIVE, None),
        ("swing", "pleasantness", SENTIC, -0.04),
        ("swing", "attention", SENTIC, 0.127),
        ("swing", "sensitivity", SENTIC, -0.12),
        ("swing", "aptitude", SENTIC, 0.223),
        ("swing", "polarity", SENTIC, 0.061),
    ]

    expected_edges = set(
        sentic_edge(subject=sentic_id(c, CONCEPT), object_=sentic_id(r, rt), weight=w)
        for (c, r, rt, w) in expected_edge_tuples
    )
    return expected_edges


@pytest.fixture
def sentic_zip_url():
    return "https://mowgli.com/sentic_test_data.zip"
