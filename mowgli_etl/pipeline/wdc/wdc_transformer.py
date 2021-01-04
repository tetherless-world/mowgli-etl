import json
from pathlib import Path
from typing import Generator, Set, Dict, Union, Optional
from urllib.parse import quote

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode

from mowgli_etl._transformer import _Transformer
from mowgli_etl.pipeline.wdc.wdc_constants import *
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_size_buckets import WdcSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_half_order_size_buckets import WdcHalfOrderSizeBuckets

import itertools


class WdcTransformer(_Transformer):
    """
    Transformer implementaion for WebDataCommons dataset using qualitative spatial reasoning predicates
    """

    def __find_predicate(self, product1, product2):
        # Placeholder predicates
        # MUCH_SMALLER_THAN = "/r/MuchSmallerThan"
        SMALLER_THAN = "/r/SmallerThan"
        EQUIVALENT_TO = "/r/EquivalentTo"
        LARGER_THAN = "/r/LargerThan"
        # MUCH_LARGER_THAN = "/r/MuchLargerThan"
        CANT_COMPARE = "/r/Can'tCompare"
        """
        Find the appropriate predicate for two WdcProductSize objects
        """
        pred = None
        if not product1.bucket or not product2.bucket:
            pred = CANT_COMPARE
        elif product1.bucket > product2.bucket:
            pred = LARGER_THAN
        elif product1.bucket < product2.bucket:
            pred = SMALLER_THAN
        else:
            pred = EQUIVALENT_TO
        return KgEdge.with_generated_id(
            subject=product1.name,
            object=product2.name,
            predicate=pred,
            source_ids=(WDC_DATASOURCE_ID,),
        )

    def transform(
        self,
        *,
        corpus: WdcOffersCorpus,
        product_type_classifier: Optional[WdcProductTypeClassifier] = None,
        dimension_parser: Optional[WdcDimensionParser] = None,
        bucketer: Optional[WdcSizeBuckets] = None,
    ) -> Generator[Union[KgNode, KgEdge], None, None]:
        """
        Main functionality for transformer

        :param corpus: container for data points for easier parsing
        :param product_type_classifier: classifier used to determine the appropriate generic product category, defaults to None
        :param dimension_parser: parser used to determine dimensions, defaults to None
        :param bucketer: algorithm for finding generalized product type sizes and bucketing them accordingly
        :return: KgEdge objects representing spatial relations between products
        """

        # Set default ProductTypeClassifier
        if not product_type_classifier:
            product_type_classifier = WdcHeuristicProductTypeClassifier()

        # Set default DimensionParser
        if not dimension_parser:
            dimension_parser = WdcParsimoniousDimensionParser()

        if not bucketer:
            bucketer = WdcHalfOrderSizeBuckets()

        self.__dimension_parser = dimension_parser
        self.__product_type_classifier = product_type_classifier
        self.__bucketer = bucketer

        # Parse file and generalize product types
        for entry in corpus.entries():
            for parsed_dimensions in self.__dimension_parser.parse(entry=entry):
                for product_type in self.__product_type_classifier.classify(
                    entry=entry
                ):
                    if not product_type or not product_type.expected:
                        continue
                    self.__bucketer.generalize(
                        wdc_product_type=product_type,
                        wdc_product_dimensions=parsed_dimensions.dimensions,
                    )

        for permutation in itertools.permutations(self.__bucketer.averages.values(), 2):
            print(permutation)
            yield self.__find_predicate(permutation[0], permutation[1])
