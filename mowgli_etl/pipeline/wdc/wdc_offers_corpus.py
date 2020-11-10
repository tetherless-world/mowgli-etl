from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


@dataclass(init=False)
class WdcOffersCorpus:
	entries: Optional[List[WdcOffersCorpusEntry]]

	def __init__(self, *, wdc_json_file_path: Path):
		self.entries = []
		for row in open(wdc_json_file_path):
			self.entries.append(WdcOffersCorpusEntry.from_json(row))

	def sample(self, n: int):
		if n < 1:
			print(f"ERROR: Desired number of lines {n} is not a positive integer")
			return None
		if n > len(self.entries):
			print(f"ERROR: Desired number of lines {n} is beyond the number of entries {len(self.entries)}")
			return None
		step_size = len(self.entries)//n
		for i in range(0, len(self.entries), step_size):
			yield self.entries[i]
		return None
