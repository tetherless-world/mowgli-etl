from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_node_visitor import (
    WdcParsimoniousNodeVisitor,
)

from parsimonious import Grammar
import dataclasses, json
from typing import Optional


class WdcParsimoniousDimensionParser(WdcDimensionParser):

    @dataclasses.dataclass
    class ParseResults:
        dimensions: Optional[WdcProductDimensions] = None
        field: Optional[str] = None
        raw_text: Optional[str] = None

    SOURCE_KEY = {
        "description": 1 / 2,
        "spec_table_content": 3 / 4,
        "key_value_pairs": 1,
    }
    __GRAMMAR = Grammar(
        """
					bin 			= (space/alt/unit/dimensions/dimension/weight/power/complex/decimal/direction/mass/current/number/word)*

					unit			= dimension space ('cm'/'in'/'ft'/'mm'/'m')
                    weight          = (decimal/number) space mass
                    power           = (decimal/number) space current
					dimensions 		= (dimension space "x" space)+ dimension
					dimension 		= (decimal/number) space direction
                    complex         = number+ space number+ space number+
                    decimal         = number+ space number+
					direction 		= ("h"/"w"/"d"/"l") &separator
                    mass            = ("lbs"/"lb"/"oz"/"kg"/"mg"/"g") &separator
                    current         = ('kv'/'mv'/'v') &separator
					number 			= ~'[0-9]+'
					word 			= ~'[A-z]*'
                    separator       = (space/~'$')
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
                and retVal.weight is None
                and retVal.power is None
            ):
                return None
            return WdcParsimoniousDimensionParser.ParseResults(dimensions = retVal)

        if entry.key_value_pairs is not None:
            for key in ("dimensions", "weight"):
                if key in entry.key_value_pairs.keys():
                    key_value_pairs = self.__GRAMMAR.parse(entry.key_value_pairs[key])
                    result = __generate_dimensions(key_value_pairs)
                    if result:
                        result.field = "key_value_pairs"
                        result.raw_text = entry.key_value_pairs
                        returns.append(result)

        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            result = __generate_dimensions(description)
            if result:
                result.field = "description"
                result.raw_text = entry.description
                returns.append(result)

        if entry.spec_table_content is not None:
            spec_table_content = self.__GRAMMAR.parse(entry.spec_table_content)
            result = __generate_dimensions(spec_table_content)
            if result:
                result.field = "spec_table_content"
                result.raw_text = entry.spec_table_content
                returns.append(result)

        return returns


if __name__ == "__main__":
    import sys, time, csv

    start = time.time()

    count = 0
    items = 0
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
                    for k, v in dataclasses.asdict(dimension.dimensions).items()
                    if v is not None
                }
                holder["dimensions"].append(clean_result)
                holder["dimensions"][-1]["accuracy"] = dimension.dimensions.accuracy(
                    WdcParsimoniousDimensionParser.SOURCE_KEY[dimension.field]
                )
                holder["dimensions"][-1]["line"] = count
                holder["dimensions"][-1]["field"] = dimension.field
                holder["dimensions"][-1]["bin"] = dimension.raw_text
                items += 1

        with open(f"{sys.argv[1][0:-6]}_parsed.csv", "w") as output:
            fields = [
                "source",
                "text",
                "depth",
                "depth_text",
                "depth_unit",
                "depth_unit_text",
                "height",
                "height_text",
                "height_unit",
                "height_unit_text",
                "length",
                "length_text",
                "length_unit",
                "length_unit_text",
                "width",
                "width_text",
                "width_unit",
                "width_unit_text",
                "weight",
                "weight_text",
                "weight_unit",
                "weight_unit_text",
                "power",
                "power_text",
                "power_unit",
                "power_unit_text",
                "accuracy",
                "line",
                "field",
                "bin"
            ]
            writer = csv.DictWriter(output, fields)
            writer.writeheader()
            for entry in holder["dimensions"]:
                for key in (
                    "width",
                    "height",
                    "length",
                    "depth",
                    "power",
                    "weight"
                ):
                    entry["source"] = holder["source"]
                    if key in entry.keys() and type(entry[key]) is dict:
                        entry[f"{key}_unit"] = entry[key]["unit"]
                        entry[f"{key}_unit_text"] = entry[key]["unit_text"]
                        entry[f"{key}_text"] = entry[key]["value_text"]
                        entry[key] = entry[key]["value"]
                writer.writerow(entry)

    print(
        f"Took {time.time()-start} seconds to run {count} parses with {items} positive results"
    )
