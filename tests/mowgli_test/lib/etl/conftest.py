import os.path
from pathlib import Path

import pytest

from mowgli.lib.etl.pipeline_storage import PipelineStorage


@pytest.fixture
def cskg_edges_csv_file_path():
    return os.path.dirname(__file__) / Path("cskg") / Path("edges.csv")


@pytest.fixture
def cskg_nodes_csv_file_path():
    return os.path.dirname(__file__) / Path("cskg") / Path("nodes.csv")


@pytest.fixture
def pipeline_storage(tmp_path_factory):
    """
    Return a file pipeline storage wrapping a test directory that is removed after testing.
    """
    yield PipelineStorage(root_data_dir_path=tmp_path_factory.mktemp("test"), pipeline_id="test")
