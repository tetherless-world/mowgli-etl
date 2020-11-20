from typing import Optional, List, Generator
from pathlib import Path
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


class WdcOffersCorpus:
    """
    Container for data source used to generate and access data entries easily

    :param wdc_json_file_path: directory of data source
    """

    def __init__(self, *, wdc_json_file_path: Path):
        """
        Constructor method
        """

        self.__file_path = wdc_json_file_path
        self.__file_length = 0
        with open(self.__file_path) as data:
            for line in data:
                self.__file_length += 1

    def entries(self) -> Generator[WdcOffersCorpusEntry, None, None]:
        """
        Access entries from corpus

        :return: entries generated from each line in the data source
        """

        with open(self.__file_path) as data:
            for row in data:
                yield WdcOffersCorpusEntry.from_json(row)

    def sample(self, n: int) -> Generator[WdcOffersCorpusEntry, None, None]:
        """
        Randomly sample entries from the corpus to simplify testing and exploration

        :param n: number of desired entries such that 0 < n < length of file
        :return: entries generated from randomly selected lines
        :raises ValueError: n is not a valid integer value between 0 and length of file
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
