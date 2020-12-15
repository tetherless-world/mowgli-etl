from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus

SOURCE_KEY = {"description": 1 / 2, "spec_table_content": 3 / 4, "key_value_pairs": 1}


def test_parsimonious_parser_large(wdc_large_offers_corpus: WdcOffersCorpus):
    for count, entry in enumerate(wdc_large_offers_corpus.entries()):
        if count in (19,20):
            dimension = WdcParsimoniousDimensionParser().parse(entry=entry)
            if not dimension:
                continue
            dimension = dimension[0]
            assert dimension.dimensions.weight.value == 1.0
            assert dimension.dimensions.weight.unit == "g"
            assert dimension.dimensions.accuracy(SOURCE_KEY[dimension.field]) == 0.75

        elif count in (79,80):
            dimension = WdcParsimoniousDimensionParser().parse(entry=entry)
            if not dimension:
                continue
            dimension = dimension[0]
            assert dimension.dimensions.weight.value == 1.7
            assert dimension.dimensions.weight.unit == "oz"
            assert dimension.dimensions.accuracy(SOURCE_KEY[dimension.field]) == 0.5
