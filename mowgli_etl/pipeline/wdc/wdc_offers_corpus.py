from typing import Optional, List, Generator
from pathlib import Path
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


class WdcOffersCorpus:
    def __init__(self, *, wdc_json_file_path: Path):
        """
        Establish collection of product entries in dataclass enclosures
        Parameters: wdc_json_file_path - Path object to data source
        """

        self.__file_path = wdc_json_file_path
        self.__file_length = open(self.__file_path).read().count("\n") + 1

    def entries(self) -> Generator[WdcOffersCorpusEntry, None, None]:
        """
        Access entries from corpus
        Yield: WdcOffersCorpusEntry - entry generated from each line in the data source
        """

        with open(self.__file_path) as data:
            for row in data:
                yield WdcOffersCorpusEntry.from_json(row)

    def sample(self, n: int) -> Generator[WdcOffersCorpusEntry, None, None]:
        """
        Randomly sample entries from the corpus to simplify testing and exploration
        Parameters: n - int number of entries desired such that 0 < n < file_length
        Yields: WdcOffersCorpusEntry - entry generated from randomly selected lines 
        """

        if n < 1:
            raise ValueError(
                f"ERROR: Desired number of lines {n} is not a positive integer"
            )
        if n > self.__file_length:
            raise ValueError(
                f"ERROR: Desired number of lines {n} is beyond the number of entries {self.__file_length}"
            )
        step_size = self.__file_length // n
        for i, entry in enumerate(self.entries()):
            if (i + 1) % step_size == 0:
                yield entry
