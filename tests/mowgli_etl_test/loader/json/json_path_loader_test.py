from itertools import islice

from mowgli_etl.loader.json.json_path_loader import JsonPathLoader
from mowgli_etl.model.kg_path import KgPath
from mowgli_etl.pipeline_storage import PipelineStorage
import json


def test_load_path(pipeline_storage: PipelineStorage):
    with JsonPathLoader().open(pipeline_storage) as loader:
        loader.load_kg_path(KgPath(source_ids=("test_datasource",), id="test_path", path=("x", "y", "z")))
    file_path = pipeline_storage.loaded_data_dir_path / "paths.json"
    assert file_path.stat().st_size > 0
    with open(file_path) as json_file:
        paths = json.load(json_file)
        assert isinstance(paths, list)
        assert len(paths) > 0
