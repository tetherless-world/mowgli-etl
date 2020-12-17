from mowgli_etl.pipeline.wdc.wdc_half_order_size_buckets import WdcHalfOrderSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_offers_corpus import WdcOffersCorpus
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.parsimonious_parser.wdc_parsimonious_dimension_parser import (
    WdcParsimoniousDimensionParser as WPDP,
)
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier as WHPTC,
)

import csv
import pandas as pd
from time import time

from sys import argv

assert __name__ == "__main__"

corpus = WdcOffersCorpus(
    wdc_json_file_path=WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl"
)
writer = pd.ExcelWriter("buckets.xlsx", engine="xlsxwriter")

if len(argv) < 2:
    volumes = (80000, 82688, 100000)
    max_buckets = 1000
else:
    max_buckets = int(argv[1])
    volumes = map(lambda x: float(x), argv[2:])

start = time()
for volume in (80000, 82688, 100000):
    for num_buckets in range(1,100,2):
        print(f"Testing: Volume={volume}, buckets={num_buckets}")
        soft_start = time()
        buckets = dict()
        for current_bucket in range(num_buckets):
            buckets[f"Bucket{current_bucket+1}"] = []
        bucketer = WdcHalfOrderSizeBuckets(num_buckets=num_buckets, max_volume=volume)
        dim_parser = WPDP()
        type_parser = WHPTC()
        for entry in corpus.entries():
            for dimension in dim_parser.parse(entry=entry):
                for product_type in type_parser.classify(entry=entry):
                    if not product_type or not product_type.expected:
                        continue
                    bucketer.generalize(wdc_product_type=product_type, wdc_product_dimensions=dimension.dimensions)

        for key in bucketer.averages.keys():
            if not bucketer.averages[key].bucket:
                continue
            buckets[f"Bucket{bucketer.averages[key].bucket}"].append((key, bucketer.averages[key].volume))

        for key in buckets.keys():
            print(f"{key} contains {len(buckets[key])} products")

        lengths = [len(buckets[key]) for key in buckets.keys()]
        num_items = sum(lengths)
        max_length = max(lengths)

        for key in buckets.keys():
            buckets[key] += [("","")]*(max_length-len(buckets[key]))

        df = pd.DataFrame(buckets)
        df.to_excel(writer, sheet_name=f"{num_buckets},{volume}")

        print(f"It took {time()-soft_start:.2f} seconds to place {num_items} items into {num_buckets} buckets")

writer.save()

# buckets = {
#     "Bucket1": [],
#     "Bucket2": [],
#     "Bucket3": [],
#     "Bucket4": [],
#     "Bucket5": [],
# }
# bucketer = WdcHalfOrderSizeBuckets()
# dim_parser = WPDP()
# type_parser = WHPTC()
# for entry in corpus.entries():
#     for dimension in dim_parser.parse(entry=entry):
#         for product_type in type_parser.classify(entry=entry):
#             if not product_type or not product_type.expected:
#                 continue
#             bucketer.generalize(wdc_product_type=product_type, wdc_product_dimensions=dimension.dimensions)

# for key in bucketer.averages.keys():
#     if not bucketer.averages[key].bucket:
#         continue
#     buckets[f"Bucket{bucketer.averages[key].bucket}"].append(
#         (key, bucketer.averages[key].volume)
#     )

# for key in buckets.keys():
#     print(f"{key} contains {len(buckets[key])} products")

# num_items = sum(len(buckets[key]) for key in buckets.keys())

# max_length = max([len(item) for item in buckets.values()])
# for key in buckets.keys():
#     while len(buckets[key]) < max_length:
#         buckets[key].append(("", ""))

# keys = sorted(buckets.keys())
# with open("buckets.csv", "w", newline="\n") as f:
#     writer = csv.writer(f)
#     writer.writerow(keys)
#     for i in range(max_length):
#         row = [
#             f"{buckets[key][i][0]} (volume: {buckets[key][i][1]})"
#             if buckets[key][i][0] != ""
#             else ""
#             for key in keys
#         ]
#         writer.writerow(row)

print(f"Wrote {num_items} items into 5 buckets in {time()-start:.2f} seconds")
