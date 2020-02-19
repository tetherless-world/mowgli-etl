from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.usf.usf_transformer import USFTransformer
from mowgli.lib.etl.usf.usf_extractor import USFExtractor

class UsfPipeline(_Pipeline):

    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=USFExtractor(),
            id = "usf",
            transformer=USFTransformer(),
            **kwds
        )







