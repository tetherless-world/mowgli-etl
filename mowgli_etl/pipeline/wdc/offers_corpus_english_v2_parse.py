import json
import spacy
import re
from os import listdir

print("\nLoading NLP library...")
nlp = spacy.load("en_core_web_sm")

# Generate a list of all possible jsonl files
directory = [item for item in listdir() if "clean.jsonl" in item]
if not directory:
	print("Sorry, there don't seem to be any clean files. Please make sure to run offers_corpus_english_v2_clean.py, or have a file ending in \"clean.jsonl\"")
	exit(1)

# Present options for jsonl files
print("Please choose which of the following files you'd like to clean [enter number on the left]:\n")
for i in range(0, len(directory)):
	print("\t{} - {}".format(i, directory[i]))

# Have user select which file to clean
choice = directory[int(input("\nChosen file number: "))]
print()

data = []

# Read the source data file into a list of JSON data objects
with open(choice) as file:
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
	category = line["category"]

	# Ignore product if there is no title
	if text == None:
		print("Insufficient data for product #{}\n".format(count))
		count += 1
		continue;

	# Tokenize title
	doc = nlp(text)

	last_noun_name = ""

	first_noun_sequence_name = ""
	first_noun_flag = 0

	last_noun_sequence_name = ""
	last_noun_flag = 1

	for token in doc:
		if token.pos in range(92, 101):
			# Assume that general product name is last noun in title (token.pos between 92 and 100 inclusive)
			last_noun_name = token.text

			# Assume that general product name is the first sequence of just nouns (token.pos between 92 and 100 inlcusive)
			# Make sure it's the first sequence
			if first_noun_flag == 0:
				if first_noun_sequence_name != "":
					first_noun_sequence_name += " "
				first_noun_sequence_name += token.text
		
			# Assume that general product name is the last sequence of just nouns (token.pos between 92 and 100 inclusive)	
			# Check if we hit a new noun sequence
			if last_noun_flag == 1:
				last_noun_sequence_name = ""
				last_noun_flag = 0
			if last_noun_sequence_name != "":
				last_noun_sequence_name += " "
			last_noun_sequence_name += token.text
		
		# Throw flag to reset last_noun_sequence
		else:
			# Throw flag to terminate first_noun_sequence
			if first_noun_sequence_name != "":
				first_noun_flag = 1
			last_noun_flag = 1

	first_noun_sequence_name.rstrip(" ")

	"""
	*
	* TO DO: Implement last_noun_sequence heuristic
	*
	"""

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
	print(text)
	print("Using the last-noun heuristic: ", end='')
	if (last_noun_name == ""):
		print("No product name found.")
	else:
		print("The product is \"{}\"".format(last_noun_name), end=".\n")

	print("Using the first-noun-sequence heuristic: ", end='')
	if (first_noun_sequence_name == ""):
		print("No product name found.")
	else:
		print("The product is \"{}\"".format(first_noun_sequence_name), end=".\n")

	print("Using the last-noun-sequence heuristic: ", end='')
	if (last_noun_sequence_name == ""):
		print("No product name found.")
	else:
		print("The product is \"{}\"".format(last_noun_sequence_name), end=".\n")


	if len(dimensions) == 0:
		print("No dimensions found.", end="\n\n")
	else:
		print("Dimensions:", dimensions[0], end="\n\n")

	count += 1