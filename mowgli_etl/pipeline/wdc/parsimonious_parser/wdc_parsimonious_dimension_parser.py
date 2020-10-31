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
    SOURCE_KEY = {
        "description": 1 / 2,
        "spec_table_content": 3 / 4,
        "key_value_pairs": 1,
    }
    __GRAMMAR = Grammar(
        """
					bin 			= (space/alt/unit/dimensions/dimension/weight/power/decimal/direction/mass/current/number/word)*

					unit			= dimension space ('cm'/'in'/'ft'/'mm'/'m')
                    weight          = (decimal/number) space mass
                    power           = (decimal/number) space current
					dimensions 		= (dimension space "x" space)+ dimension
					dimension 		= (decimal/number) space direction
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
            return retVal

        if entry.key_value_pairs is not None:
            for key in ("dimensions", "weight"):
                if key in entry.key_value_pairs.keys():
                    key_value_pairs = self.__GRAMMAR.parse(entry.key_value_pairs[key])
                    result = __generate_dimensions(key_value_pairs)
                    if result:
                        returns.append(
                            (result, "key_value_pairs", entry.key_value_pairs)
                        )

        if entry.description is not None:
            description = self.__GRAMMAR.parse(entry.description)
            result = __generate_dimensions(description)
            if result:
                returns.append((result, "description", entry.description))

        if entry.spec_table_content is not None:
            spec_table_content = self.__GRAMMAR.parse(entry.spec_table_content)
            result = __generate_dimensions(spec_table_content)
            if result:
                returns.append((result, "spec_table_content", entry.spec_table_content))

        return returns


if __name__ == "__main__":
    import sys, time

    MODE = "json"
    if len(sys.argv) >= 3:
        MODE = sys.argv[2]

    start = time.time()

    if MODE in ("json", "csv"):
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
                        for k, v in dataclasses.asdict(dimension[0]).items()
                        if v is not None
                    }
                    holder["dimensions"].append(clean_result)
                    holder["dimensions"][-1]["accuracy"] = dimension[0].accuracy(
                        WdcParsimoniousDimensionParser.SOURCE_KEY[dimension[1]]
                    )
                    holder["dimensions"][-1]["line"] = count
                    holder["dimensions"][-1]["field"] = dimension[1]
                    holder["dimensions"][-1]["raw_text"] = dimension[2]
                    items += 1
            if MODE == "json":
                import json

                with open(f"{sys.argv[1][0:-6]}_parsed.jsonl", "w") as output:
                    json.dump(holder, output, indent=4)
            elif MODE == "csv":
                import csv

                with open(f"{sys.argv[1][0:-6]}_parsed.csv", "w") as output:
                    fields = [
                        "source",
                        "raw_text",
                        "depth",
                        "depth_unit",
                        "height",
                        "height_unit",
                        "length",
                        "length_unit",
                        "width",
                        "width_unit",
                        "weight",
                        "weight_unit",
                        "power",
                        "power_unit",
                        "accuracy",
                        "line",
                        "field",
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
                            "weight",
                        ):
                            entry["source"] = holder["source"]
                            if key in entry.keys() and type(entry[key]) is dict:
                                entry[f"{key}_unit"] = entry[key]["unit"]
                                entry[key] = entry[key]["value"]
                        writer.writerow(entry)

    elif MODE == "print":
        count = 0
        items = 0
        with open(WDC_ARCHIVE_PATH / sys.argv[1], "r") as data:
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
                            if (
                                getattr(data, f.name) is not None
                                and getattr(data, f.name).value is not None
                            ):
                                output += f"\n{spacing}{f.name}:"
                                values = getattr(data, f.name)
                                if type(values).__name__ == "__Dimension":
                                    for subf in dataclasses.fields(values):
                                        if (
                                            getattr(values, subf.name) is not None
                                            or subf.name == "unit"
                                        ):
                                            output += f"\n{spacing}{spacing}{subf.name}: {getattr(values, subf.name)}"
                                else:
                                    output += f" {getattr(data, f.name)}"
                        if output != "":
                            items += 1
                            print(
                                f"NEW DIMENSION OBJECT from entry {count}{output}".strip()
                            )
                            if len(sys.argv) >= 3 and sys.argv[2] == "origin":
                                print("\nWhich was produced from:\n")
                                print(d[1])

    print(
        f"Took {time.time()-start} seconds to run {count} parses with {items} positive results"
    )
