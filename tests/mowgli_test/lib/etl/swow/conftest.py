import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path


@pytest.fixture
def sample_swow_strengths_path():
    return Path(__file__).parent / 'sample_swow_strengths.csv'


@pytest.fixture
def sample_swow_nodes_path():
    return Path(__file__).parent / 'sample_swow_nodes.csv'


@pytest.fixture
def sample_swow_edges_path():
    return Path(__file__).parent / 'sample_swow_edges.csv'


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
