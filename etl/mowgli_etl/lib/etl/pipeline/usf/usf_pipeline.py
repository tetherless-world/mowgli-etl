from mowgli_etl.lib.etl._pipeline import _Pipeline
from mowgli_etl.lib.etl.pipeline.usf.usf_extractor import USFExtractor
from mowgli_etl.lib.etl.pipeline.usf.usf_transformer import USFTransformer


class UsfPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=USFExtractor(**kwds),
            id="usf",
            transformer=USFTransformer(),
            **kwds
        )
