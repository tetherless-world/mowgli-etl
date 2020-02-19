import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path

_sample_usf_file_path = Path(__file__).parent / 'usf_test_data.xml'

@pytest.fixture
def strengths():
    return open(_sample_usf_file_path)

@pytest.fixture
def url():
    return "https://github.com/dfamilia33/usf_test_data/archive/master.zip"