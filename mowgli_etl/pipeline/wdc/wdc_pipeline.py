from configargparse import ArgParser

from mowgli_etl._pipeline import _Pipeline
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID
from mowgli_etl.pipeline.wdc.wdc_extractor import WdcExtractor
from mowgli_etl.pipeline.wdc.wdc_transformer import WdcTransformer


class WdcPipeline(_Pipeline):
    """
    ETL pipeline that extracts from the Web Data Commons corpus.

    https://webdatacommons.org
    """

    def __init__(self, product_type_classifier: str, **kwds):
        # if product_type_classifier == "heuristic":
        #     product_type_classifier_inst = WdcHeuristicProductTypeClassifier()
        # # elif product_type_classifier == "spacy":
        # #     product_type_classifier_inst = ...
        # else:
        #     raise NotImplementedError(product_type_classifier)

        _Pipeline.__init__(
            self,
            extractor=WdcExtractor(),
            id=WDC_DATASOURCE_ID,
            transformer=WdcTransformer(),  # product_type_classifier=product_type_classifier_inst),
            **kwds
        )

    def add_arguments(cls, arg_parser: ArgParser) -> None:
        _Pipeline.add_arguments(arg_parser)
        arg_parser.add_argument("--product-type-classifier", default="heuristic")
