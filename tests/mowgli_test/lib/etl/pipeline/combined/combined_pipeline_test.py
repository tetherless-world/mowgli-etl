from itertools import islice

from mowgli.lib.etl.pipeline.combined.combined_pipeline import CombinedPipeline
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_test.lib.etl.etl_mocks import MockTransformer, MockPipeline


def test_combined_pipeline(pipeline_storage, graph_generator):
    rows_per_pipeline = 6

    pipelines = tuple(
        MockPipeline(id=f'pipe_{pipe_num}',
                     transformer=MockTransformer(tuple(islice(graph_generator, rows_per_pipeline))))
        for pipe_num in range(1, 4)
    )

    combined_pipeline = CombinedPipeline(pipelines=pipelines, serial=True)

    wrapper = PipelineWrapper(combined_pipeline, pipeline_storage)
    extract_kwds = wrapper.extract()
    transform_result = wrapper.transform(**extract_kwds)

    graph = tuple(transform_result)
    assert len(graph) == len(pipelines) * rows_per_pipeline
