import json
from pathlib import Path
from typing import Generator, Set, Dict, Union, Optional
from urllib.parse import quote
import re
import spacy
import os.path

# from mowgli_etl.model.concept_net_predicates import
from mowgli_etl.model.kg_edge import KgEdge

# from mowtli_etl.model.mowgli_predicates import
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


class WdcTransformer(_Transformer):

    def transform(
        self,
        *,
        wdc_jsonl_file_path: Path,
        wdc_product_type_classifier: Optional[WdcProductTypeClassifier] = None,
        wdc_dimension_parser: Optional[WdcDimensionParser] = None
    ) -> Generator[Union[KgNode, KgEdge], None, None]:
        # Prepare file and nlp
        wdc_clean_file_path = self.__clean(wdc_jsonl_file_path)

        # Set default ProductTypeClassifier
        if not wdc_product_type_classifier:
            wdc_product_type_classifier = WdcHeuristicProductTypeClassifier()

        # Set default DimensionParser
        if not wdc_dimension_parser:
            wdc_dimension_parser = WdcParsimoniousDimensionParser()

        self.__dimension_parser = wdc_dimension_parser
        self.__product_type_classifier = wdc_product_type_classifier

        # Parse file
        with open(wdc_clean_file_path) as data:
            for row in data:
                entry = WdcOffersCorpusEntry.from_json(row)
                product_type = next(
                    self.__product_type_classifier.classify(
                        entry=entry
                    )
                )
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