from mowgli import paths
from os.path import isdir

def test_src_root_exists():
    assert isdir(paths.SRC_ROOT)

def test_project_root_exists():
    assert isdir(paths.PROJECT_ROOT)

def test_data_dir_exists():
    assert isdir(paths.DATA_DIR)