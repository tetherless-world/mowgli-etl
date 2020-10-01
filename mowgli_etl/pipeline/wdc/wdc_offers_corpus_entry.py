from dataclasses import dataclass
from typing import Optional, List

from dataclasses_json import dataclass_json

from mowgli_etl.loader import json
from mowgli_etl.paths import DATA_DIR


@dataclass_json
@dataclass(frozen=True)
class _WdcOffersCorpusEntryIdentifier:
    sku: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class WdcOffersCorpusEntry:
    brand: Optional[str]
    category: Optional[str]
    cluster_id: int
    description: Optional[str]
    id: int
    identifiers: Optional[List[_WdcOffersCorpusEntryIdentifier]]
    # {"brand":null,"category":"Clothing","cluster_id":3617395,"description":null,"id":210,"identifiers":[{"\/sku":"[codesku17smmtzi50x]"}],"keyValuePairs":null,"price":null,"specTableContent":null,"title":"selce zip t shirt montura maungashop"}


if __name__ == "__main__":
    with open(
        DATA_DIR / "wdc" / "extracted" / "offers_corpus_english_v2_1000.jsonl"
    ) as offers_corpus_jsonl_file:
        for line in offers_corpus_jsonl_file:
            entry = WdcOffersCorpusEntry.from_json(line)
            # print(entry)
            print(entry.to_json())
