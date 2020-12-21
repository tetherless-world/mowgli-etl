from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_naive_size_buckets import WdcNaiveSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser,
)


def test_wdc_naive_size_buckets(wdc_large_offers_corpus: WdcOffersCorpus):
    bucketer = WdcNaiveSizeBuckets()
    type_parser = WdcHeuristicProductTypeClassifier()
    dimension_parser = WdcParsimoniousDimensionParser()
    for entry in wdc_large_offers_corpus.entries():
        for dimension in dimension_parser.parse(entry=entry):
            for product in type_parser.classify(entry=entry):
                if not product or not product.expected:
                    continue
                bucketer.generalize(
                    wdc_product_type=product,
                    wdc_product_dimensions=dimension.dimensions,
                )
    for generic_product in bucketer.averages.values():
        if generic_product.bucket:
            assert type(generic_product.bucket) in (float, int)
            assert generic_product.bucket == generic_product.volume
