import random

with open("offers_corpus_english_v2_1000.jsonl") as file:
	lines = random.sample(file.readlines(), 100)

with open("offers_corpus_english_v2_random_100.jsonl", "w") as file:
	for line in lines:
		file.write(line)