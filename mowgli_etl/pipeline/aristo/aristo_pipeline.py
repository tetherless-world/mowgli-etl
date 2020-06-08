from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.aristo.aristo_extractor import AristoExtractor
from mowgli_etl.pipeline.aristo.aristo_transformer import AristoTransformer


class AristoPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=AristoExtractor(),
            id="aristo",
            transformer=AristoTransformer(),
            **kwds
        )
