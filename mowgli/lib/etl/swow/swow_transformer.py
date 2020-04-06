import csv
from typing import Generator, Union, Dict

from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.swow.swow_constants import SWOW_CSV_FILE_KEY
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node
from mowgli.lib.etl._transformer import _Transformer

_NOT_AVAILABLE_TERM = "NA"


class SwowTransformer(_Transformer):
    """ 
    Transforms SWOW relations from a csv file into cskg nodes/edges.
    """

    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a SWOW csv file.
        """
        words = {}
        associations = {}
        if SWOW_CSV_FILE_KEY not in kwds:
            raise ValueError(f"No SWOW csv file found for key {SWOW_CSV_FILE_KEY}")
        with open(kwds[SWOW_CSV_FILE_KEY], mode="r") as csv_file:
            csv_reader = csv.DictReader(
                csv_file,
                delimiter=",",
                quotechar='"',
                doublequote=True,
                skipinitialspace=True,
            )
            for row in csv_reader:
                raw_cue = row["cue"]
                cue_word = words.setdefault(raw_cue, _SwowWord(raw_cue))
                for resp_num in range(1, 4):
                    resp_type = f"R{resp_num}"
                    raw_resp = row[resp_type]
                    if raw_resp == _NOT_AVAILABLE_TERM:
                        continue
                    resp_word = words.setdefault(raw_resp, _SwowWord(raw_resp))
                    assoc_key = (raw_cue, raw_resp)
                    association = associations.setdefault(
                        assoc_key, _SwowAssociation(cue_word, resp_word)
                    )
                    cue_word.increment_resp_count(resp_type)
                    association.increment_resp_count(resp_type)
        for word in words.values():
            yield word.to_cskg_node()

        for association in associations.values():
            yield association.to_cskg_edge()


class _SwowWord:
    def __init__(self, word):
        self.__word = word
        self.__response_counts = {}

    def increment_resp_count(self, resp_type: str):
        self.__response_counts.setdefault(resp_type, 0)
        self.__response_counts[resp_type] += 1

    def resp_count(self, resp_type) -> int:
        return self.__response_counts.get(resp_type, 0)

    @property
    def total_responses(self) -> int:
        return sum(resp_count for resp_count in self.__response_counts.values())

    @property
    def word(self) -> str:
        return self.__word

    def to_cskg_node(self):
        return swow_node(self.__word)


class _SwowAssociation:
    def __init__(self, cue: _SwowWord, resp: _SwowWord):
        self.__cue = cue
        self.__resp = resp
        self.__responded_counts = {}

    def increment_resp_count(self, resp_type: str):
        self.__responded_counts.setdefault(resp_type, 0)
        self.__responded_counts[resp_type] += 1

    def to_cskg_edge(self):
        r123 = sum(resp_count for resp_count in self.__responded_counts.values())
        r123_strength = r123 / self.__cue.total_responses
        return swow_edge(
            cue=self.__cue.word, response=self.__resp.word, strength=r123_strength
        )
