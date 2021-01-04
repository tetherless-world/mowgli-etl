from typing import Optional, List, Generator
from pathlib import Path
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry
from langdetect import detect


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
                if self.__valid_line(line):
                    self.__file_length += 1

    def __valid_line(self, line):
        return detect(line) == "en"

    def entries(self) -> Generator[WdcOffersCorpusEntry, None, None]:
        """
        Access entries from corpus

        :return: entries generated from each line in the data source
        """

        with open(self.__file_path) as data:
            for row in data:
                if self.__valid_line(row):
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
        counter = 0
        for i, entry in enumerate(self.entries()):
            if (i + 1) % step_size == 0:
                counter += 1
                yield entry
                # Special break in case of uneven split
                if counter == n:
                    return
