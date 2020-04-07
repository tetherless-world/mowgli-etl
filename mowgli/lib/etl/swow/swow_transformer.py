import csv
from typing import Generator, Union, Dict

from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.etl.swow.swow_constants import SWOW_CSV_FILE_KEY
from mowgli.lib.etl.swow.swow_mappers import swow_edge, swow_node, SwowResponseCounter
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
        # Track response counts for each word
        word_resp_counts = {}
        # Track response counts for each cue->response association
        assoc_resp_counts = {}
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
                cue = row["cue"]
                cue_resp_counter = word_resp_counts.setdefault(
                    cue, SwowResponseCounter()
                )
                for resp_type in ("R1", "R2", "R3"):
                    response = row[resp_type]
                    if response == _NOT_AVAILABLE_TERM:
                        continue
                    # ensure that the response word is registered as a node
                    word_resp_counts.setdefault(response, SwowResponseCounter())
                    assoc_resp_counter = assoc_resp_counts.setdefault(
                        (cue, response), SwowResponseCounter()
                    )
                    cue_resp_counter.increment_resp_count(resp_type)
                    assoc_resp_counter.increment_resp_count(resp_type)

        for word, resp_counts in word_resp_counts.items():
            yield swow_node(word=word, response_counts=resp_counts)

        for (cue, response), resp_counts in assoc_resp_counts.items():
            cue_resp_counts = word_resp_counts[cue]
            yield swow_edge(
                cue=cue,
                cue_response_counts=cue_resp_counts,
                response=response,
                response_counts=resp_counts,
            )
