import os.path
from pathlib import Path

import pytest

from mowgli.lib.etl.pipeline_storage import PipelineStorage


@pytest.fixture
def cskg_csv_dir_path():
    return os.path.dirname(__file__) / Path("cskg")


@pytest.fixture
def pipeline_storage(tmp_path_factory):
    """
    Return a file pipeline storage wrapping a test directory that is removed after testing.
    """
    yield PipelineStorage(root_data_dir_path=tmp_path_factory.mktemp("test"), pipeline_id="test")
