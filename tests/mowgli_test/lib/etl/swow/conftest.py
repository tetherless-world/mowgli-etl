import bz2
from pathlib import Path

import pytest
from io import TextIOWrapper
from pathlib import Path

from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node


@pytest.fixture
def sample_swow_csv_path():
    return Path(__file__).parent / "sample_swow_data.csv"


@pytest.fixture
def sample_swow_nodes():
    expected_node_names = [
        "a",
        "one",
        "b",
        "c",
        "indefinite article",
        "a few",
        "beers",
        "more",
        "bee",
        "yourself",
    ]
    expected_nodes = set(swow_node(name) for name in expected_node_names)
    return expected_nodes


@pytest.fixture
def sample_swow_edges():
    expected_edge_tuples = [
        ("a", "one", 2 / 5),
        ("a", "b", 1 / 5),
        ("a", "c", 1 / 5),
        ("a", "indefinite article", 1 / 5),
        ("a few", "beers", 1 / 2),
        ("a few", "more", 1 / 2),
        ("b", "bee", 2 / 6),
        ("b", "c", 1 / 6),
        ("b", "a", 2 / 6),
        ("b", "yourself", 1 / 6),
    ]
    expected_edges = set(
        swow_edge(cue=c, response=r, strength=s) for (c, r, s) in expected_edge_tuples
    )
    return expected_edges


@pytest.fixture
def sample_archive_path(sample_swow_csv_path, tmp_path_factory):
    """
    Generate a bz2 archive from the sample strengths file and return the path.
    Remove the file on clean up.
    """
    with open(sample_swow_csv_path, mode="rb") as f:
        compressed = bz2.compress(f.read())
        sample_bz2_path = (
            tmp_path_factory.mktemp("swow-test") / "sample_swow_csv.csv.bz2"
        )
        with open(sample_bz2_path, mode="wb") as bz2_file:
            bz2_file.write(compressed)
        yield sample_bz2_path
        sample_bz2_path.unlink()
