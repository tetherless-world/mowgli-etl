import json
import sys

from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_node_visitor import (
    WdcParsimoniousNodeVisitor,
)

from parsimonious import Grammar


class WdcParsimoniousDimensionParser(WdcDimensionParser):
    def __init__(self):
        self.__GRAMMAR = Grammar(
            """
						bin 			= (space/unit/decimal/dimensions/dimension/direction/number/word)*

						unit			= dimension space ('cm'/'in'/'ft'/'mm'/'m')
                        decimal         = number+ space number+
						dimensions 		= (dimension space "x" space)+ dimension
						dimension 		= (number+/decimal) space direction
						direction 		= ("h"/"w"/"d"/"l") &(space/~'$')
						number 			= ~'[0-9]+'
						word 			= ~'[A-z]*'
						space			= ~'\s'
						"""
        )
        self.__VISITOR = WdcParsimoniousNodeVisitor()

    def parse(self, *, entry: WdcOffersCorpusEntry):
        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            self.__VISITOR.visit(description)
            if self.__VISITOR.dictionary.keys():
                print(self.__VISITOR.dictionary)


if __name__ == "__main__":
    with open(
        WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r"
    ) as data:
        count = 0
        for row in data:
            count += 1
            WdcParsimoniousDimensionParser().parse(
                entry=WdcOffersCorpusEntry.from_json(row)
            )
