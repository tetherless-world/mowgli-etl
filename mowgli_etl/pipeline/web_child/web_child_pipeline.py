from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.web_child.web_child_extractor import WebChildExtractor
from mowgli_etl.pipeline.web_child.web_child_transformer import WebChildTransformer


class WebChildPipeline(_Pipeline):
    def __init__(self, **kwds):
        _Pipeline.__init__(
            self,
            extractor=WebChildExtractor(**kwds),
            id="web_child",
            transformer=WebChildTransformer(),
            **kwds
        )

    @classmethod
    def add_arguments(cls, arg_parser):
        _Pipeline.add_arguments(arg_parser)
