from mowgli_etl.pipeline.food_on.food_on_pipeline import FoodOnPipeline
from mowgli_etl.pipeline_wrapper import PipelineWrapper


def test_food_on_pipeline(pipeline_storage):
    pipeline = FoodOnPipeline()
    pipeline_wrapper = PipelineWrapper(pipeline, pipeline_storage)

    pipeline_wrapper.run(force=False)
