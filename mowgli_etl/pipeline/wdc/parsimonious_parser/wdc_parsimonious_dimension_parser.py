import json
import sys

from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_node_visitor import (
    WdcParsimoniousNodeVisitor,
)

import dataclasses

from parsimonious import Grammar


class WdcParsimoniousDimensionParser(WdcDimensionParser):
    def __init__(self):
        self.__GRAMMAR = Grammar(
            """
						bin 			= (space/unit/dimensions/dimension/decimal/direction/number/word)*

						unit			= dimension space ('cm'/'in'/'ft'/'mm'/'m')
						dimensions 		= (dimension space "x" space)+ dimension
						dimension 		= (decimal/number) space direction
                        decimal         = number+ space number+
						direction 		= ("h"/"w"/"d"/"l") &(space/~'$')
						number 			= ~'[0-9]+'
						word 			= ~'[A-z]*'
						space			= ~'\s'
						"""
        )
        self.__VISITOR = WdcParsimoniousNodeVisitor()

    def __generate_dimensions(self):
        retVal = WdcProductDimensions.from_dict(self.__VISITOR.dictionary)
        self.__VISITOR.dictionary = {}
        return retVal

    def parse(self, *, entry: WdcOffersCorpusEntry):
        returns = []
        return_flag = False
        if entry.keyValuePairs is not None:
            if "dimensions" in entry.keyValuePairs.keys():
                keyValuePairs = self.__GRAMMAR.parse(entry.keyValuePairs["dimensions"])
                self.__VISITOR.visit(keyValuePairs)
                returns.append(
                    (self.__generate_dimensions(), keyValuePairs)
                )

        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            self.__VISITOR.visit(description)
            returns.append((self.__generate_dimensions(), description))

        return returns


if __name__ == "__main__":
    with open(
        WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r"
    ) as data:
        count = 0
        for row in data:
            count += 1
            dimension = WdcParsimoniousDimensionParser().parse(
                entry=WdcOffersCorpusEntry.from_json(row)
            )
            if dimension:
                for d in dimension:
                    output = ""
                    spacing = "\t"
                    data = d[0]
                    for f in dataclasses.fields(data):
                        if getattr(data, f.name) is not None:
                            output += f"{spacing}{f.name}: {getattr(data,f.name)}\n"
                    if output != "":
                        print(f"NEW DIMENSION OBJECT from entry {count}\n{output}".strip())
                        if len(sys.argv) >= 2 and sys.argv[1] == "origin":
                            print("\nWhich was produced from:\n")
                            print(d[1])
