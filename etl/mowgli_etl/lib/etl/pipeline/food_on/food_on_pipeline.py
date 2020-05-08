from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl.pipeline.food_on.food_on_extractor import FoodOnExtractor
from mowgli_etl.lib.etl.pipeline.food_on.food_on_transformer import FoodOnTransformer


class FoodOnPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=FoodOnExtractor(),
            id="food_on",
            transformer=FoodOnTransformer(),
            **kwds
        )
