import json
from pathlib import Path
from typing import Generator, Set, Dict, Union, Optional
from urllib.parse import quote
import re
import spacy
import os.path

from mowgli_etl.model.kg_edge import KgEdge

from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.word_net_id import WordNetId
from mowgli_etl.pipeline.wdc.wdc_constants import (
    WDC_DATASOURCE_ID,
    WDC_HAS_DIMENSIONS,
    WDC_ARCHIVE_PATH,
)
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus


class WdcTransformer(_Transformer):
    """
    Transformer implementaion for WebDataCommons dataset using qualitative spatial reasoning predicates
    """

    def transform(
        self,
        *,
        corpus: WdcOffersCorpus,
        product_type_classifier: Optional[WdcProductTypeClassifier] = None,
        dimension_parser: Optional[WdcDimensionParser] = None
    ) -> Generator[Union[KgNode, KgEdge], None, None]:
        """
        Main functionality for transformer

        :param corpus: container for data points for easier parsing
        :param product_type_classifier: classifier used to determine the appropriate generic product category, defaults to None
        :param dimension_parser: parser used to determine dimensions, defaults to None
        :return: KgEdge objects representing spatial relations between products
        """

        # Set default ProductTypeClassifier
        if not product_type_classifier:
            product_type_classifier = WdcHeuristicProductTypeClassifier()

        # Set default DimensionParser
        if not dimension_parser:
            dimension_parser = WdcParsimoniousDimensionParser()

        self.__dimension_parser = dimension_parser
        self.__product_type_classifier = product_type_classifier

        # Parse file
        for entry in corpus.entries():
            product_type = next(self.__product_type_classifier.classify(entry=entry))
            parsed_dimensions = next(self.__dimension_parser.parse(entry=entry))

            if product_type.expected:
                yield KgEdge.with_generated_id(
                    subject=product_type.expected.name,
                    predicate=WDC_HAS_DIMENSIONS,
                    object="NA",
                    source_ids=(WDC_DATASOURCE_ID,),
                )
            else:
                yield KgEdge.with_generated_id(
                    subject="NA",
                    predicate=WDC_HAS_DIMENSIONS,
                    object="NA",
                    source_ids=(WDC_DATASOURCE_ID,),
                )
