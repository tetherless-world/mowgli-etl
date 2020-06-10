from itertools import islice

from mowgli_etl.loader.json.json_edge_loader import JsonEdgeLoader
from mowgli_etl.model.edge import Edge
from mowgli_etl.pipeline_storage import PipelineStorage
import json


def test_load_edge(graph_generator, pipeline_storage: PipelineStorage):
    with JsonEdgeLoader().open(pipeline_storage) as loader:
        for edge in islice(graph_generator, 100):
            if isinstance(edge, Edge):
                loader.load_edge(edge)
    file_path = pipeline_storage.loaded_data_dir_path / "edges.json"
    assert file_path.stat().st_size > 0
    with open(file_path) as json_file:
        edges = json.load(json_file)
        assert isinstance(edges, list)
        assert len(edges) > 0
