from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline.has_part.has_part_extractor import HasPartExtractor
from mowgli.lib.etl.pipeline.has_part.has_part_transformer import HasPartTransformer


class HasPartPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=HasPartExtractor(),
            id="has_part",
            transformer=HasPartTransformer(),
            **kwds
        )
