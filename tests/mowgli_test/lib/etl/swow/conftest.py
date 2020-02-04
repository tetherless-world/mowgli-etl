import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path

_sample_swow_strengths_path = Path(__file__).parent / 'sample_swow_strengths.csv'

@pytest.fixture
def sample_swow_strengths():
    return open(_sample_swow_strengths_path)

@pytest.fixture
def sample_archive_path():
    """
    Generate a bz2 archive from the sample strengths file and return the path.
    Remove the file on clean up.
    """
    with open(_sample_swow_strengths_path, mode='rb') as f:
        compressed = bz2.compress(f.read())
        current_dir = Path(__file__).parent
        sample_bz2_path = current_dir / 'sample_swow_strengths.csv.bz2'
        with open(sample_bz2_path, mode='wb') as bz2_file:
            bz2_file.write(compressed)
        yield sample_bz2_path
        sample_bz2_path.unlink()
