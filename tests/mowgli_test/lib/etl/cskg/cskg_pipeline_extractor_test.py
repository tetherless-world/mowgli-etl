import os
from itertools import islice

from mowgli.lib.etl.combined.combined_pipeline_extractor import CombinedPipelineExtractor
from tests.mowgli_test.lib.etl.etl_mocks import MockPipeline, MockTransformer


def test_cskg_pipeline_extractor(pipeline_storage, graph_generator):
    pipelines = tuple(
        MockPipeline(id=f'pipe_{pipe_num}', transformer=MockTransformer(islice(graph_generator, 6)))
        for pipe_num in range(1, 4)
    )

    pipeline_extractor = CombinedPipelineExtractor(pipelines=pipelines)
    extract_kwds = pipeline_extractor.extract(force=False, storage=pipeline_storage)

    node_paths = extract_kwds['nodes_csv_file_paths']
    assert len(node_paths) == len(pipelines)
    for node_path in node_paths:
        assert os.path.isfile(node_path)

    edge_paths = extract_kwds['edges_csv_file_paths']
    assert len(edge_paths) == len(pipelines)
    for edge_path in edge_paths:
        os.path.isfile(edge_path)
