from json import loads
from pathlib import Path

from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry

SOURCE_KEY = {"description": 1 / 2, "spec_table_content": 3 / 4, "key_value_pairs": 1}

def test_parsimonious_parser_large(wdc_large_json_file_path: Path):
    with open(wdc_large_json_file_path, "r") as data:
        for count, entry in enumerate(data):
            count += 1
            entry = WdcOffersCorpusEntry.from_json(entry)
            if count == 24:
                dimension = WdcParsimoniousDimensionParser().parse(entry=entry)[0]
                assert dimension.dimensions.weight.value == 1.0
                assert dimension.dimensions.weight.unit == "g"
                assert (
                    dimension.dimensions.accuracy(SOURCE_KEY[dimension.field]) == 0.75
                )

            elif count == 88:
                dimension = WdcParsimoniousDimensionParser().parse(entry=entry)[0]
                assert dimension.dimensions.weight.value == 1.7
                assert dimension.dimensions.weight.unit == "oz"
                assert dimension.dimensions.accuracy(SOURCE_KEY[dimension.field]) == 0.5

            elif count == 191:
                dimensions = WdcParsimoniousDimensionParser().parse(entry=entry)
                assert dimensions[0].dimensions.weight.value == 10.92
                assert dimensions[0].dimensions.weight.unit == "lbs"
                assert (
                    dimensions[0].dimensions.accuracy(SOURCE_KEY[dimensions[0].field])
                    == 1
                )

                assert dimensions[1].dimensions.weight.value == 368.0
                assert dimensions[1].dimensions.weight.unit == "g"
                assert (
                    dimensions[1].dimensions.accuracy(SOURCE_KEY[dimensions[1].field])
                    == 0.75
                )
