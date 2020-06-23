from mowgli_etl.pipeline.mcs_benchmark.mcs_benchmark_pipeline import McsBenchmarkPipeline
from mowgli_etl.pipeline_wrapper import PipelineWrapper


def test_mcs_benchmark_pipeline(pipeline_storage):
    pipeline = McsBenchmarkPipeline()
    wrapper = PipelineWrapper(pipeline, pipeline_storage)
    wrapper.run()
