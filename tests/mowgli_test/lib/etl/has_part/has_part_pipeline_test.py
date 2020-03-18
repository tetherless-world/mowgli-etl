from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from tests.mowgli_test.lib.etl.has_part.has_part_pipeline import HasPartPipeline


def test_has_part_pipeline(pipeline_storage):
    pipeline = HasPartPipeline()
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)

    pipeline_wrapper.extract_transform_load(force=False)
