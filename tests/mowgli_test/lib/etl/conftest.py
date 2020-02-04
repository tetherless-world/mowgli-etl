from pathlib import Path
import pytest
from shutil import rmtree

from mowgli.lib.etl.file_pipeline_storage import FilePipelineStorage

_test_file_storage_path = Path(__file__).parent / '.test_file_pipeline_storage'

@pytest.fixture
def pipeline_storage():
    """
    Return a file pipeline storage wrapping a test directory that is removed after testing.
    """
    assert not _test_file_storage_path.exists()
    _test_file_storage_path.mkdir()
    yield FilePipelineStorage.create(_test_file_storage_path)
    rmtree(_test_file_storage_path)
