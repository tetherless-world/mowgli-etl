from typing import Optional, List, Generator
from pathlib import Path
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


class WdcOffersCorpus:
	def __init__(self, *, wdc_json_file_path: Path):
		self.__file_path = wdc_json_file_path
		self.__file_length = open(self.__file_path).read().count('\n') + 1

	def entries(self) -> Generator[WdcOffersCorpusEntry, None, None]:
		with open(self.__file_path) as data:
			for row in data:
				yield WdcOffersCorpusEntry.from_json(row)

	def sample(self, n: int):
		if n < 1:
			raise ValueError(f"ERROR: Desired number of lines {n} is not a positive integer")
		if n > self.__file_length:
			raise ValueError(f"ERROR: Desired number of lines {n} is beyond the number of entries {self.__file_length}")
		step_size = self.__file_length//n
		for i, entry in enumerate(self.entries()):
			if i+1 % step_size == 0:
				yield entry
		return None
