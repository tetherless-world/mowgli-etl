from itertools import islice

from mowgli_etl.loader.json.json_node_loader import JsonNodeLoader
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline_storage import PipelineStorage
import json


def test_load_node(graph_generator, pipeline_storage: PipelineStorage):
    with JsonNodeLoader().open(pipeline_storage) as loader:
        for node in islice(graph_generator, 100):
            if isinstance(node, KgNode):
                loader.load_node(node)
    file_path = pipeline_storage.loaded_data_dir_path / "nodes.json"
    assert file_path.stat().st_size > 0
    with open(file_path) as json_file:
        nodes = json.load(json_file)
        assert isinstance(nodes, list)
        assert len(nodes) > 0
