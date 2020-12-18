from mowgli_etl.pipeline.wdc.wdc_half_order_size_buckets import WdcHalfOrderSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_naive_size_buckets import WdcNaiveSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_rounded_size_buckets import WdcRoundedSizeBuckets

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

print("USAGE: file -h/--heuristic CamelString -mb/--min-buckets int -Mb/--max-buckets int -bs/--bucket-step int -v/--volumes float float float ...")

def sort_dataframe(df):
    return df.reindex(sorted(df.columns, key=lambda x: float(x[6:])), axis=1)

KNOWN_HEURISTICS = ["HalfOrder", "Naive", "Rounded",]
print(f"Known heuristics: {', '.join(KNOWN_HEURISTICS)}")

volumes = (80000, 82688, 100000)
min_buckets = 1
max_buckets = 100
bucket_step = 2
heuristic = "HalfOrder"

i = 1
while i < len(argv):
    if argv[i] in ("-h", "--heuristic"):
        if argv[i+1] in KNOWN_HEURISTICS:
            heuristic = argv[i+1]
        else:
            print(f"WARNING: {argv[i+1]} is not a known heuristic")
        i += 2
    elif argv[i] in ("-mb", "--min-buckets"):
        min_buckets = int(argv[i+1])
        i += 2
    elif argv[i] in ("-Mb", "--max-buckets"):
        max_buckets = int(argv[i+1])
        i += 2
    elif argv[i] in ("-bs", "--bucket-step"):
        bucket_step = int(argv[i+1])
        i += 2
    elif argv[i] in ("-v", "--volumes"):
        volumes = map(lambda x: float(x), argv[i+1:])
        i += 2
    else:
        break

corpus = WdcOffersCorpus(
    wdc_json_file_path=WDC_ARCHIVE_PATH / "offers_corpus_english_v2_1000.jsonl"
)
writer = pd.ExcelWriter(f"{heuristic}_buckets.xlsx", engine="xlsxwriter")

start = time()
print(f"Testing: {heuristic} buckets")

# Single pass heuristics
if heuristic in ("Naive", "Rounded"):
    soft_start = time()
    bucketer = None
    if heuristic == "Naive":
        bucketer = WdcNaiveSizeBuckets()
    elif heuristic == "Rounded":
        bucketer = WdcRoundedSizeBuckets()
    buckets = dict()
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
        bucket_string = f"Bucket{bucketer.averages[key].bucket}"
        if bucket_string not in buckets.keys():
            buckets[bucket_string] = []
        buckets[bucket_string].append((key, bucketer.averages[key].volume))

    for key in buckets.keys():
        print(f"{key} contains {len(buckets[key])} products")

    lengths = [len(buckets[key]) for key in buckets.keys()]
    num_items = sum(lengths)
    max_length = max(lengths)

    for key in buckets.keys():
        buckets[key] += [""]*(max_length-len(buckets[key]))

    df = pd.DataFrame(buckets)
    df = sort_dataframe(df)
    df.to_excel(writer, sheet_name=f"{heuristic} buckets")

    print(f"It took {time()-soft_start:.2f} seconds to place {num_items} in {len(buckets.keys())} buckets")

# Multiple pass heuristics
else:
    for volume in volumes:
        for num_buckets in range(min_buckets,max_buckets,bucket_step):
            print(f"Testing: Volume={volume}, {heuristic} buckets={num_buckets}")
            soft_start = time()
            buckets = dict()
            bucketer = None
            if heuristic == "HalfOrder":
                bucketer = WdcHalfOrderSizeBuckets(num_buckets=num_buckets, max_volume=volume)
            else:
                break
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
                bucket_string = f"Bucket{bucketer.averages[key].bucket}"
                if bucket_string not in buckets.keys():
                    buckets[bucket_string] = []
                buckets[bucket_string].append((key, bucketer.averages[key].volume))

            for key in buckets.keys():
                print(f"{key} contains {len(buckets[key])} products")

            lengths = [len(buckets[key]) for key in buckets.keys()]
            num_items = sum(lengths)
            max_length = max(lengths)

            for key in buckets.keys():
                buckets[key] += [""]*(max_length-len(buckets[key]))

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
