from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)
from mowgli_etl.pipeline.wdc.wdc_half_order_size_buckets import WdcHalfOrderSizeBuckets

from math import log


def test_wdc_half_order_size_buckets(wdc_large_offers_corpus: WdcOffersCorpus):
    bucketer = WdcHalfOrderSizeBuckets()
    product_parser = WdcHeuristicProductTypeClassifier()
    dimension_parser = WdcParsimoniousDimensionParser()
    for entry in wdc_large_offers_corpus.entries():
        for product in product_parser.classify(entry=entry):
            if not product or not product.expected:
                continue
            for dimension in dimension_parser.parse(entry=entry):
                bucketer.generalize(
                    wdc_product_type=product,
                    wdc_product_dimensions=dimension.dimensions,
                )
    for generic_product in bucketer.averages.values():
        if not generic_product.bucket:
            continue
        assert type(generic_product.bucket) in (float, int)
        assert generic_product.bucket == 1 or generic_product.bucket - 1 <= (
            bucketer.num_buckets - 1
        ) * (log(generic_product.volume * 10 / bucketer.max_volume) / log(10))
