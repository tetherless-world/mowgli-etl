from mowgli.lib.etl.has_part.has_part_pipeline import HasPartPipeline
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper


def test_has_part_pipeline(pipeline_storage):
    pipeline = HasPartPipeline()
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)

    pipeline_wrapper.extract_transform_load(force=False)
