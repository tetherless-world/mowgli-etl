from pathlib import Path
from json import loads

from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier
)
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry

# Should have Path argument, for now using clean file already in directory
def test_heuristic_product_type_classifier_clean(wdc_json_clean_file_path: Path):
    with open(wdc_json_clean_file_path) as data:
        HPTC = WdcHeuristicProductTypeClassifier()
        for count, row in enumerate(data):
            if count+1 == 2:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Clothing"
                assert f"{item.expected.confidence:.3%}" == "100.000%"
            elif count+1 in [3,4]:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Sports"
                assert f"{item.expected.confidence:.3%}" == "100.000%"
            elif count+1 == 5:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Office Products"
                assert f"{item.expected.confidence:.3%}" == "66.667%"

def test_heuristic_product_type_classifier_large(wdc_large_json_file_path: Path):
    with open(wdc_large_json_file_path) as data:
        HPTC = WdcHeuristicProductTypeClassifier()
        for count, row in enumerate(data):
            if count+1 == 1:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Electronics"
                assert f"{item.expected.confidence:.3%}" == "100.000%"
            elif count+1 == 2:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Jewelry"
                assert f"{item.expected.confidence:.3%}" == "100.000%"
            elif count+1 == 3:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Gourmet Food"
                assert f"{item.expected.confidence:.3%}" == "33.333%"
            elif count+1 == 5:
                item = next(HPTC.classify(entry=WdcOffersCorpusEntry.from_json(row)))
                assert item.expected.name == "Photo"
                assert f"{item.expected.confidence:.3%}" == "66.667%"
