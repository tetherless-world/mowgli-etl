import os
from itertools import islice

from mowgli.lib.etl.cskg.cskg_pipeline_extractor import CskgPipelineExtractor
from tests.mowgli_test.lib.etl.etl_mocks import MockPipeline, MockTransformer


def test_cskg_pipeline_extractor(tmp_path_factory, graph_generator):
    test_root = tmp_path_factory.mktemp('cskg_test_root')

    pipelines = tuple(
        MockPipeline(id=f'pipe_{pipe_num}', transformer=MockTransformer(islice(graph_generator, 6)))
        for pipe_num in range(1, 4)
    )

    pipeline_extractor = CskgPipelineExtractor(root_data_dir_path=test_root, pipelines=pipelines)
    extract_kwds = pipeline_extractor.extract(force=False)

    node_paths = extract_kwds['nodes_csv_file_paths']
    assert len(node_paths) == len(pipelines)
    for node_path in node_paths:
        assert os.path.isfile(node_path)

    edge_paths = extract_kwds['edges_csv_file_paths']
    assert len(edge_paths) == len(pipelines)
    for edge_path in edge_paths:
        os.path.isfile(edge_path)
