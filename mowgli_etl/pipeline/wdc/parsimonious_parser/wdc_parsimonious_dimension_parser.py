from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_node_visitor import (
    WdcParsimoniousNodeVisitor,
)

from parsimonious import Grammar
import dataclasses, json


class WdcParsimoniousDimensionParser(WdcDimensionParser):
    __GRAMMAR = Grammar(
        """
					bin 			= (space/alt/unit/dimensions/dimension/decimal/direction/number/word)*

					unit			= dimension space ('cm'/'in'/'ft'/'mm'/'m')
					dimensions 		= (dimension space "x" space)+ dimension
					dimension 		= (decimal/number) space direction
                    decimal         = number+ space number+
					direction 		= ("h"/"w"/"d"/"l") &(space/~'$')
					number 			= ~'[0-9]+'
					word 			= ~'[A-z]*'
					space			= ~'\s'
					alt             = ~'[^a-zA-Z\d\s:]'
                    """
    )

    def parse(self, *, entry: WdcOffersCorpusEntry):
        returns = []
        return_flag = False
        __VISITOR = WdcParsimoniousNodeVisitor()

        def __generate_dimensions(source):
            __VISITOR = WdcParsimoniousNodeVisitor()
            __VISITOR.visit(source)
            retVal = WdcProductDimensions.from_dict(
                dataclasses.asdict(__VISITOR.dictionary)
            )
            if (
                retVal.width is None
                and retVal.length is None
                and retVal.depth is None
                and retVal.height is None
            ):
                return None
            return retVal

        if entry.key_value_pairs is not None:
            if "dimensions" in entry.key_value_pairs.keys():
                key_value_pairs = self.__GRAMMAR.parse(
                    entry.key_value_pairs["dimensions"]
                )
                result = __generate_dimensions(key_value_pairs)
                if result:
                    returns.append((result, "key_value_pairs", entry.key_value_pairs))

        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            result = __generate_dimensions(description)
            if result:
                returns.append((result, "description", entry.description))

        return returns


if __name__ == "__main__":
    import json, sys, time

    start = time.time()
    count = 0
    with open(WDC_ARCHIVE_PATH / sys.argv[1], "r") as data:
        holder = {"source": sys.argv[1], "dimensions": []}
        for row in data:
            count += 1
            dimensions = WdcParsimoniousDimensionParser().parse(
                entry=WdcOffersCorpusEntry.from_json(row)
            )
            for dimension in dimensions:
                clean_result = {
                    k: v
                    for k, v in dataclasses.asdict(dimension[0]).items()
                    if v is not None
                }
                holder["dimensions"].append(clean_result)
                holder["dimensions"][-1]["line"] = count
                holder["dimensions"][-1]["field"] = dimension[1]
                holder["dimensions"][-1]["raw_text"] = dimension[2]
        with open(f"{sys.argv[1][0:-6]}_parsed.jsonl", "w") as output:
            json.dump(holder, output, indent=4)

        # count = 0
        # for row in data:
        #     count += 1
        #     dimension = WdcParsimoniousDimensionParser().parse(
        #         entry=WdcOffersCorpusEntry.from_json(row)
        #     )
        #     if dimension:
        #         for d in dimension:
        #             output = ""
        #             spacing = "\t"
        #             data = d[0]
        #             for f in dataclasses.fields(data):
        #                 if getattr(data, f.name) is not None and getattr(data, f.name).value is not None:
        #                     output += f"\n{spacing}{f.name}:"
        #                     values = getattr(data, f.name)
        #                     if type(values).__name__ == "__Dimension":
        #                         for subf in dataclasses.fields(values):
        #                             if (
        #                                 getattr(values, subf.name) is not None
        #                                 or subf.name == "unit"
        #                             ):
        #                                 output += f"\n{spacing}{spacing}{subf.name}: {getattr(values, subf.name)}"
        #                     else:
        #                         output += f" {getattr(data, f.name)}"
        #             if output != "":
        #                 print(
        #                     f"NEW DIMENSION OBJECT from entry {count}{output}".strip()
        #                 )
        #                 if len(sys.argv) >= 3 and sys.argv[2] == "origin":
        #                     print("\nWhich was produced from:\n")
        #                     print(d[1])
    print(f"Took {time.time()-start} seconds to run {count} parses")
