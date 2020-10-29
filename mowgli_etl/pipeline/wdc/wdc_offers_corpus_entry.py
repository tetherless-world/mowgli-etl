from dataclasses import dataclass, field
from typing import Optional, List

from dataclasses_json import dataclass_json, config

from mowgli_etl.loader import json
from mowgli_etl.paths import DATA_DIR


@dataclass_json
@dataclass(frozen=True)
class WdcOffersCorpusEntry:
    @dataclass_json
    @dataclass(frozen=True)
    class __WdcOffersCorpusEntryIdentifier:
        gtin8: Optional[str] = None
        gtin12: Optional[str] = None
        gtin13: Optional[str] = None
        gtin14: Optional[str] = None
        identifier: Optional[str] = None
        mpn: Optional[str] = None
        productID: Optional[str] = None
        sku: Optional[str] = None

    brand: Optional[str]
    category: Optional[str]
    cluster_id: int
    description: Optional[str]
    id: int
    identifiers: Optional[List[__WdcOffersCorpusEntryIdentifier]]
    key_value_pairs: Optional[dict] = field(metadata=config(field_name="keyValuePairs"))
    spec_table_content: Optional[str] = field(metadata=config(field_name="specTableContent"))
    # {"brand":null,"category":"Clothing","cluster_id":3617395,"description":null,"id":210,"identifiers":[{"\/sku":"[codesku17smmtzi50x]"}],"keyValuePairs":null,"price":null,"specTableContent":null,"title":"selce zip t shirt montura maungashop"}


if __name__ == "__main__":
    with open(
        DATA_DIR / "wdc" / "extracted" / "offers_corpus_english_v2_1000.jsonl"
    ) as offers_corpus_jsonl_file:
        for line in offers_corpus_jsonl_file:
            entry = WdcOffersCorpusEntry.from_json(line)
            print(entry.identifiers)
            # print(entry.to_json())
