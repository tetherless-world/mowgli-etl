from mowgli.lib.etl._pipeline import _Pipeline
from mowgli.lib.etl.webchild.webchild_extractor import WebchildExtractor
from mowgli.lib.etl.webchild.webchild_transformer import WebchildTransformer


class WebchildPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=WebchildExtractor(**kwds),
            id="webchild",
            transformer=WebchildTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
