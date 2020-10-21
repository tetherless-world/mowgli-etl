from pathlib import Path
from json import loads

from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier as WdcHPTC,
)

# Should have Path argument, for now using clean file already in directory
def test_heuristic_prdocut_type_classifier():
    with open("offers_corpus_english_v2_random_100_clean.jsonl", "r") as data:
        item_counter = 0
        for row in data:
            item_counter += 1
            information = loads(row)
            listing = information["title"]
            description = information["description"]
            additional_info = information["specTableContent"]
            category = information["category"]

            if listing == None:
                listing = description
                if listing == None:
                    listing = category
            hpt = WdcHPTC().classify(title=listing)
            if item_counter == 1:
                assert hpt.name == "7"
                assert hpt.alternate[0] == "hella bitter citrus bitters 1 7"
                assert hpt.alternate[1] == "hella bitter citrus bitters 1 7"

            elif item_counter == 12:
                assert hpt.name == "shirt"
                assert hpt.alternate[0] == "hanes mens tagless t shirt"
                assert hpt.alternate[1] == "hanes mens tagless t shirt"
