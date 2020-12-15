from mowgli_etl.pipeline.wdc.wdc_size_buckets import WdcSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser as WPDP,
)
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier as WHPTC,
)

import csv

assert __name__ == "__main__"

buckets = {
    "Bucket1": [],
    "Bucket2": [],
    "Bucket3": [],
    "Bucket4": [],
    "Bucket5": [],
}
bucketer = WdcSizeBuckets()
corpus = WdcOffersCorpus(
    wdc_json_file_path=WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl"
)
dim_parser = WPDP()
type_parser = WHPTC()
for entry in corpus.entries():
    for dimension in dim_parser.parse(entry=entry):
        for product_type in type_parser.classify(entry=entry):
            if not product_type or not product_type.expected:
                continue
            bucketer.generalize(product_type, dimension.dimensions)

for key in bucketer.averages.keys():
    if not bucketer.averages[key].bucket:
        continue
    buckets[f"Bucket{bucketer.averages[key].bucket}"].append((key,bucketer.averages[key].volume))

for key in buckets.keys():
    print(f"{key} contains {len(buckets[key])} products")

max_length = max([len(item) for item in buckets.values()])
for key in buckets.keys():
    while len(buckets[key]) < max_length:
        buckets[key].append(('',''))

keys = sorted(buckets.keys())
with open("buckets.csv", "w", newline="\n") as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for i in range(max_length):
        row = [f"{buckets[key][i][0]} (volume: {buckets[key][i][1]})" if buckets[key][i][0] != '' else '' for key in keys]
        writer.writerow(row)

print(f"Wrote into 5 buckets")
