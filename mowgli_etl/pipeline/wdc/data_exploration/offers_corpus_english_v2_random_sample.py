from random import sample
from pathlib import Path

from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry

def data_sample(wdc_jsonl_file_path: Path, n: int) -> WdcOffersCorpusEntry:
	if n < 1:
		print(f"ERROR: Desired number of lines {n} is not a positive integer")
		return None
	with open(wdc_jsonl_file_path) as data:
		line_count = data.read().count('\n') + 1
		if n > line_count:
			print(f"ERROR: Desired number of lines {n} is beyond the length of the file {line_count}")
			return None
	with open(wdc_jsonl_file_path) as data:
		lines = sample(range(1, line_count+1), n)
		for i, row in enumerate(data):
			if i in lines:
				yield WdcOffersCorpusEntry.from_json(row)
	return None
