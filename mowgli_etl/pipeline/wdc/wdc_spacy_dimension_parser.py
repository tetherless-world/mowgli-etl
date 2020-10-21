import spacy
import json
import sys
import spacy

import dataclasses

from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH

nlp = spacy.load("en_core_web_sm")


class WdcSpacyDimensionParser(WdcDimensionParser):
    def parse(self, *, information: WdcOffersCorpusEntry):
        for field in dataclasses.fields(information):
            fieldValue = getattr(information, field.name)
            print(f"Parsing data from {field.name}...")

            if fieldValue is None:
                print("\tNoneType found")
                continue
            if type(fieldValue) is int:
                print(f"\t{fieldValue}")
                continue
            if str(type(fieldValue).__name__) == "list":
                for item in fieldValue:
                    self.parse(information=item)
                continue
            doc = nlp(fieldValue)
            for token in doc:
                print(f"\t{token}: {token.pos}")


if __name__ == "__main__":
    with open(
        WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl"
    ) as offers_corpus_jsonl_file:
        for line in offers_corpus_jsonl_file:
            print("parsing...")
            entry = WdcOffersCorpusEntry.from_json(line)
            WdcSpacyDimensionParser().parse(information=entry)
