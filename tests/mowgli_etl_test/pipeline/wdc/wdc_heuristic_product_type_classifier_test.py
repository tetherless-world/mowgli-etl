from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier,
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus

def test_heuristic_product_type_classifier(wdc_large_offers_corpus: WdcOffersCorpus):
    HPTC = WdcHeuristicProductTypeClassifier()
    for count, entry in enumerate(wdc_large_offers_corpus.entries):
        if count + 1 == 1:
            item = next(HPTC.classify(entry=entry))
            assert item.expected.name == "Electronics"
            assert f"{item.expected.confidence:.3%}" == "100.000%"
        elif count + 1 == 2:
            item = next(HPTC.classify(entry=entry))
            assert item.expected.name == "Jewelry"
            assert f"{item.expected.confidence:.3%}" == "100.000%"
        elif count + 1 == 3:
            item = next(HPTC.classify(entry=entry))
            assert item.expected.name == "Gourmet Food"
            assert f"{item.expected.confidence:.3%}" == "33.333%"
        elif count + 1 == 5:
            item = next(HPTC.classify(entry=entry))
            assert item.expected.name == "Photo"
            assert f"{item.expected.confidence:.3%}" == "66.667%"
