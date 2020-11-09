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
    WdcHeuristicProductTypeClassifier as HPTC,
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


class WdcTransformer(_Transformer):
    __BAD_DUPLICATE = '{"brand":'

    def __clean(self, wdc_jsonl_file_path: Path):
        """
        Clean input file, particularly checking for multiple json items in one line, or split json object; return file with original name + "_clean"
        """
        wdc_jsonl_dir_path, wdc_jsonl_file_name = os.path.split(wdc_jsonl_file_path)
        wdc_jsonl_file_base_name, _ext = os.path.splitext(wdc_jsonl_file_name)
        new_file_name = (
            wdc_jsonl_dir_path + "/" + wdc_jsonl_file_base_name + "_clean.jsonl"
        )

        with open(wdc_jsonl_file_path, "r") as wdc_jsonl_file_file, open(
            new_file_name, "w"
        ) as new_file:
            for line in wdc_jsonl_file_file:
                # Catch duplicate objects
                if line.count(self.__BAD_DUPLICATE) > 1:
                    temp_line = ""
                    data_starts = []
                    val = 0
                    while val != -1:
                        val = line.find(self.__BAD_DUPLICATE, val + 1)
                        if line[val - 2] == ":" or val == -1:
                            continue
                        data_starts.append(val - 1)

                    for i in range(len(data_starts)):
                        if i < len(data_starts) - 1:
                            temp_line += line[data_starts[i] : data_starts[i + 1]]
                            if temp_line[-1] != "}":
                                temp_line += "}"
                            temp_line += "\n"
                        else:
                            t = list(line[data_starts[i] : :])
                            t[0] = "{"
                            temp_line += "".join(t)

                        line = temp_line
                new_file.write(line)

        return new_file_name

    

    def transform(
        self, *, wdc_jsonl_file_path: Path, wdc_product_type_classifier: Optional[WdcProductTypeClassifier]=None, wdc_dimension_parser: Optional[WdcDimensionParser]=None
    ) -> Generator[Union[KgNode, KgEdge], None, None]:
        # Prepare file and nlp
        wdc_clean_file_path = self.__clean(wdc_jsonl_file_path)

        # # Set default ProductTypeClassifier
        # if not wdc_product_type_classifier:
        #     wdc_product_type_classifier = WdcProductTypeClassifier()

        # # Set default DimensionParser
        # if not wdc_dimension_parser:
        #     wdc_dimension_parser = WdcDimensionParser()

        self.__dimension_parser = wdc_dimension_parser
        self.__product_type_classifier = wdc_product_type_classifier

        # Parse file
        with open(wdc_clean_file_path) as data:
            for row in data:
                name = "NA"
                if self.__dimension_parser:
                    name = next(self.__product_type_classifier.classify(entry=WdcOffersCorpusEntry.from_json(row))).expected.name
                
                yield KgEdge.with_generated_id(
                    subject=name,
                    predicate=WDC_HAS_DIMENSIONS,
                    object="NA",
                    source_ids=(WDC_DATASOURCE_ID,),
                )
                