import json
import sys

from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH

from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor

class WdcNodeVisitor(NodeVisitor):
    def __init__(self):
        self.dictionary = {}

    def visit_dimension(self, node, visited_children):
        value, key = node.text.split(' ')
        self.dictionary[key] = value

    def visit_unit(self, node, visited_children):
        self.dictionary['unit'] = node.text

    def generic_visit(self, node, visited_children):
        return None

class WdcParsimoniousDimensionParser(WdcDimensionParser):
    def __init__(self):
        self.__GRAMMAR = Grammar(
            """
						bin 			= (space/unit/decimal/dimensions/dimension/direction/number/word)*

						unit			= 'cm'/'in'/'ft'/'mm'/'m'
                        decimal         = number+ space number+
						dimensions 		= (dimension space "x" space)+ dimension
						dimension 		= (number+/decimal) space direction
						direction 		= ("h"/"w"/"d"/"l")
						number 			= ~'[0-9]+'
						word 			= ~'[A-z]*'
						space			= ~'\s'
						"""
        )
        self.__VISITOR = WdcNodeVisitor()

    def parse(self, *, entry: WdcOffersCorpusEntry):
        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            self.__VISITOR.visit(description)
            print(self.__VISITOR.dictionary)


if __name__ == "__main__":
    with open(
        WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r"
    ) as data:
        count = 0
        for row in data:
            count += 1
            if count == 34:
                WdcParsimoniousDimensionParser().parse(
                    entry=WdcOffersCorpusEntry.from_json(row)
                )
