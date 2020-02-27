import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path

from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node


@pytest.fixture
def sample_swow_strengths_path():
    return Path(__file__).parent / 'sample_swow_strengths.csv'


@pytest.fixture
def sample_swow_nodes():
    expected_node_names = ['a', 'one', 'b', 'c', 'indefinite article', 'a few', 'beers', 'bee']
    expected_nodes = set(swow_node(name) for name in expected_node_names)
    return expected_nodes


@pytest.fixture
def sample_swow_edges():
    expected_edge_tuples = [
        ('a', 'one', 0.118518518518519),
        ('a', 'b', 0.0518518518518519),
        ('a', 'c', 0.0185185185185185),
        ('a', 'indefinite article', 0.00740740740740741),
        ('a few', 'beers', 0.0148698884758364),
        ('b', 'bee', 0.121863799283154),
        ('b', 'c', 0.0896057347670251),
        ('b', 'a', 0.0681003584229391)
    ]
    expected_edges = set(swow_edge(cue=c, response=r, strength=s) for (c, r, s) in expected_edge_tuples)
    return expected_edges


@pytest.fixture
def sample_archive_path(sample_swow_strengths_path, tmp_path_factory):
    """
    Generate a bz2 archive from the sample strengths file and return the path.
    Remove the file on clean up.
    """
    with open(sample_swow_strengths_path, mode='rb') as f:
        compressed = bz2.compress(f.read())
        sample_bz2_path = tmp_path_factory.mktemp("swow-test") / 'sample_swow_strengths.csv.bz2'
        with open(sample_bz2_path, mode='wb') as bz2_file:
            bz2_file.write(compressed)
        yield sample_bz2_path
        sample_bz2_path.unlink()
