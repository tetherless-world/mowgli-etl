from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.aristo.aristo_extractor import AristoExtractor
from mowgli.lib.etl.aristo.aristo_transformer import AristoTransformer


class AristoPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=AristoExtractor(),
            id="aristo",
            transformer=AristoTransformer(),
            **kwds
        )
