import bz2
from pathlib import Path

import pytest
from io import TextIOWrapper
from pathlib import Path

from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node, SwowResponseCounter


@pytest.fixture
def sample_swow_csv_path():
    return Path(__file__).parent / "sample_swow_data.csv"


def _sample_cue_counts():
    return {
        "a": SwowResponseCounter(r1=2, r2=2, r3=1),
        "a few": SwowResponseCounter(r1=1, r2=1, r3=0),
        "b": SwowResponseCounter(r1=2, r2=2, r3=2),
    }


@pytest.fixture
def sample_swow_nodes():
    cue_counts = _sample_cue_counts()
    responses = (
        "bee",
        "beers",
        "c",
        "indefinite article",
        "more",
        "one",
        "yourself",
    )
    expected_nodes = set(
        swow_node(word=word, response_counts=counter)
        for word, counter in cue_counts.items()
    )
    expected_nodes.update(
        swow_node(word=word, response_counts=SwowResponseCounter())
        for word in responses
    )
    return expected_nodes


@pytest.fixture
def sample_swow_edges():
    cue_counts = _sample_cue_counts()
    expected_edge_tuples = (
        ("a", "one", SwowResponseCounter(r1=2)),
        ("a", "b", SwowResponseCounter(r2=1)),
        ("a", "c", SwowResponseCounter(r3=1)),
        ("a", "indefinite article", SwowResponseCounter(r2=1)),
        ("a few", "beers", SwowResponseCounter(r1=1)),
        ("a few", "more", SwowResponseCounter(r2=1)),
        ("b", "bee", SwowResponseCounter(r1=1, r3=1)),
        ("b", "c", SwowResponseCounter(r2=1)),
        ("b", "a", SwowResponseCounter(r2=1, r3=1)),
        ("b", "yourself", SwowResponseCounter(r1=1)),
    )
    expected_edges = set(
        swow_edge(
            cue=cue,
            cue_response_counts=cue_counts[cue],
            response=response,
            response_counts=response_counter,
        )
        for (cue, response, response_counter) in expected_edge_tuples
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
