import os

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.cskg.cskg_pipeline_extractor import CskgPipelineExtractor
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from tests.mowgli_test.lib.etl.etl_mocks import MockTransformer, MockPipeline


def test_cskg_pipeline_extractor(tmp_path_factory):
    cskg_root_dir = tmp_path_factory.mktemp('cskg_test_dir')
    node = Node(
        datasource='test_datasource',
        id='test_nid',
        label='test node'
    )
    edge = Edge(
        datasource='test_datasource',
        object_=node,
        predicate='pred',
        subject=node
    )
    transformer = MockTransformer(nodes=[node], edges=[edge])

    pipelines = [MockPipeline(id=f'pipe_{pipe_num}', transformer=transformer) for pipe_num in range(1, 4)]

    pipeline_extractor = CskgPipelineExtractor(cskg_data_dir_path=cskg_root_dir, pipelines=pipelines)
    extract_kwds = pipeline_extractor.extract(force=False)

    node_paths = extract_kwds['nodes_csv_file_paths']
    assert len(node_paths) == len(pipelines)
    for node_path in node_paths:
        assert os.path.isfile(node_path)

    edge_paths = extract_kwds['edges_csv_file_paths']
    assert len(edge_paths) == len(pipelines)
    for edge_path in edge_paths:
        os.path.isfile(edge_path)

