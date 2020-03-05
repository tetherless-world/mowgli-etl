from itertools import islice

from mowgli.lib.etl.cskg.cskg_combined_pipeline import CskgCombinedPipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_test.lib.etl.etl_mocks import MockTransformer, MockPipeline


def test_cskg_combined_pipeline(tmp_path_factory, graph_generator):
    test_root = tmp_path_factory.mktemp('cskg_test_root')

    rows_per_pipeline = 6

    pipelines = tuple(
        MockPipeline(id=f'pipe_{pipe_num}', transformer=MockTransformer(islice(graph_generator, rows_per_pipeline)))
        for pipe_num in range(1, 4)
    )

    pipe_id = 'combined_test'
    combined_pipeline = CskgCombinedPipeline(id=pipe_id, pipelines=pipelines, root_data_dir_path=test_root)
    storage = PipelineStorage(pipeline_id=pipe_id, root_data_dir_path=test_root)

    wrapper = PipelineWrapper(combined_pipeline, storage)
    extract_kwds = wrapper.extract()
    transform_result = wrapper.transform(**extract_kwds)

    graph = tuple(_ for _ in transform_result)
    assert len(graph) == len(pipelines) * rows_per_pipeline
