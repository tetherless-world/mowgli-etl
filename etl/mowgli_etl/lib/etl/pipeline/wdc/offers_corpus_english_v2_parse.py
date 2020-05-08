import json
import spacy
import re

nlp = spacy.load("en_core_web_sm")

data = []

# Read the source data file into a list of JSON data objects
with open("offers_corpus_english_v2_random_100.jsonl") as file:
	for line in file:
		data.append(json.loads(line))

count = 1

# For each product
for line in data:
	print("Product", count)

	# Extract the three primary data fields
	text = line["title"]
	description = line["description"]
	additional_info = line["specTableContent"]

	# Ignore product if there is no title
	if text == None:
		continue;

	# Tokenize title
	doc = nlp(text)

	product_name = ""

	# Assume that general product name is last noun in title
	for token in doc:
		if token.pos_ == "NOUN":
			product_name = token.text

	dimensions = []

	# Try to identify dimensions embedded in the desciption using regular expressions
	if description != None:
		dimensions = re.findall("\d+(?: \d+)?\s?\w*\sx\s\d+(?: \d+)?\s?(?:x\s\d+\s?)?\w*", description)

		if len(dimensions) == 0:
			dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\slead\sx\s\d+\s?\w+", description)

	if len(dimensions) == 0:
		dimensions = re.findall("\d+\s?\w*\sx\s\d+\s?\w*", text)

	if len(dimensions) == 0:
		dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\slead\sx\s\d+\s?\w+", text)

	if len(dimensions) == 0:
		if additional_info != None:
			dimensions = re.findall("\d+(?: \d+)?\s?\w*\sx\s\d+(?: \d+)?\s?(?:x\s\d+\s?)?\w*", additional_info)

			if len(dimensions) == 0:
				dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\slead\sx\s\d+\s?\w+", additional_info)

	# Print out the results
	if (product_name == ""):
		print("No product name found.")
	else:
		print("The product is", product_name, end=".\n")

	if len(dimensions) == 0:
		print("No dimensions found.", end="\n\n")
	else:
		print("Dimensions:", dimensions[0], end="\n\n")

	count += 1