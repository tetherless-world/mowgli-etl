import random

from mowgli_etl.paths import DATA_DIR

with open(
    DATA_DIR / "wdc" / "extracted" / "offers_corpus_english_v2_1000.jsonl"
) as file:
    lines = random.sample(file.readlines(), 100)

with open(
    DATA_DIR / "wdc" / "extracted" / "offers_corpus_english_v2_random_100.jsonl", "w"
) as file:
    for line in lines:
        file.write(line)
