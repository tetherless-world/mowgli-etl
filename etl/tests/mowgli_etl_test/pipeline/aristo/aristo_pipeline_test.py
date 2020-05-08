from mowgli_etl.pipeline.aristo.aristo_pipeline import AristoPipeline
from mowgli_etl.pipeline_wrapper import PipelineWrapper


def test_aristo_pipeline(pipeline_storage):
    pipeline = AristoPipeline()
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)
    pipeline_wrapper.run(force=False)
