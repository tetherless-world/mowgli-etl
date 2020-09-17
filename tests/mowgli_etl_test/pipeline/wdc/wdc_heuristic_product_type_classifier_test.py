from pathlib import Path
from json import loads

from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import WdcHeuristicProductTypeClassifier as WdcHPTC

#Should have Path argument, for now using clean file already in directory
def test_heuristic_prdocut_type_classifier():
    with open("offers_corpus_english_v2_random_100_clean.jsonl","r") as data:
        for row in data:
            print(row)
            information = loads(row)
            listing = information["title"]
            description = information["description"]
            additional_info = information["specTableContent"]
            category = information["category"]

            if listing == None:
                listing=description
                if listing == None:
                    listing = category
            hpt = WdcHPTC().classify(title=listing)
            print(hpt.name,hpt.confidence,"Alternate")
            for name in hpt.alternate:
                print(f"\t{name}")
