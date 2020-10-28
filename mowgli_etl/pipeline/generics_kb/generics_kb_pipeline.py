from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.generics_kb.generics_kb_extractor import GenericsKbExtractor
from mowgli_etl.pipeline.generics_kb.generics_kb_transformer import (
    GenericsKbTransformer,
)


class GenericsKbPipeline(_Pipeline):
    ID = "generics_kb"

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=GenericsKbExtractor(),
            id=self.ID,
            transformer=GenericsKbTransformer(),
            **kwds
        )
