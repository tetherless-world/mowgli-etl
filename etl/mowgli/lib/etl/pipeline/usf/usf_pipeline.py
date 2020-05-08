from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.pipeline.usf.usf_extractor import USFExtractor
from mowgli.lib.etl.pipeline.usf.usf_transformer import USFTransformer


class UsfPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=USFExtractor(**kwds),
            id="usf",
            transformer=USFTransformer(),
            **kwds
        )
