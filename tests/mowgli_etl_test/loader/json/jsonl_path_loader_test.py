from itertools import islice

from mowgli_etl.loader.json.json_path_loader import JsonPathLoader
from mowgli_etl.loader.json.jsonl_path_loader import JsonlPathLoader
from mowgli_etl.model.kg_path import KgPath
from mowgli_etl.pipeline_storage import PipelineStorage
import json


def test_load_path(pipeline_storage: PipelineStorage):
    with JsonlPathLoader().open(pipeline_storage) as loader:
        loader.load_kg_path(
            KgPath(
                source_ids=("test_datasource",),
                id="test_path1",
                path=("x1", "y1", "z1"),
            )
        )
        loader.load_kg_path(
            KgPath(
                source_ids=("test_datasource",),
                id="test_path2",
                path=("x2", "y2", "z2"),
            )
        )
    file_path = pipeline_storage.loaded_data_dir_path / "paths.jsonl"
    assert file_path.stat().st_size > 0
    with open(file_path) as jsonl_file:
        for line in jsonl_file:
            path = json.loads(line)
            assert isinstance(path, dict)
            assert path["id"].startswith("test_path")
