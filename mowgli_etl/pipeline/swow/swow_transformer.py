import csv
from collections import Counter
from pathlib import Path
from typing import Generator, Union

from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl._transformer import _Transformer
from mowgli_etl.pipeline.swow.swow_mappers import swow_edge, swow_node, SwowResponseType

_NOT_AVAILABLE_TERM = "NA"


class SwowTransformer(_Transformer):
    """
    Transforms SWOW relations from a csv file into cskg nodes/edges.
    """

    def transform(
        self, *, swow_csv_file: Path
    ) -> Generator[Union[Node, Edge], None, None]:
        """
        Generate nodes and edges from a SWOW csv file.
        """
        edge_tree = {}
        with open(swow_csv_file, mode="r") as csv_file:
            csv_reader = csv.DictReader(
                csv_file,
                delimiter=",",
                quotechar='"',
                doublequote=True,
                skipinitialspace=True,
            )
            for row in csv_reader:
                cue = row["cue"]
                for resp_type in SwowResponseType.__members__.keys():
                    response = row[resp_type]
                    if response == _NOT_AVAILABLE_TERM:
                        continue
                    edge_counter = edge_tree.setdefault(cue, {}).setdefault(
                        response, Counter()
                    )
                    edge_counter[resp_type] += 1
                    # ensure that the response word is registered as a node
                    edge_tree.setdefault(response, {})

        for cue, associations in edge_tree.items():
            total_resp_counts = sum(associations.values(), Counter())
            yield swow_node(word=cue, response_counts=total_resp_counts)
            for response, resp_counts in associations.items():
                yield swow_edge(
                    cue=cue,
                    cue_response_counts=total_resp_counts,
                    response=response,
                    response_counts=resp_counts,
                )
