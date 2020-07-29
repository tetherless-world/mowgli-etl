import random
import os

# new_path = os.path.relpath("../../../data//wdc/extract/offers_corpus_english_v2_1000.jsonl")
with open(os.path.dirname(__file__) + "../../../data/wdc/extracted/offers_corpus_english_v2_1000.jsonl") as file:
	lines = random.sample(file.readlines(), 100)

with open("offers_corpus_english_v2_random_100.jsonl", "w") as file:
	for line in lines:
		file.write(line)