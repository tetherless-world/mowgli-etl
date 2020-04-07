from typing import Union, Optional
from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import SWOW_DATASOURCE_ID, SWOW_NAMESPACE

""" 
Utility methods for mapping SWOW data into MOWGLI CSKG data structures.
"""


class SwowResponseCounter:
    def __init__(self, r1: int = 0, r2: int = 0, r3: int = 0):
        self.__counts = {"R1": r1, "R2": r2, "R3": r3}

    def increment_resp_count(self, key: str):
        if key not in self.__counts:
            raise KeyError(f"Invalid response key: {key}")
        self.__counts[key] += 1

    @property
    def counts(self):
        return self.__counts.copy()


def swow_node_id(word: str) -> str:
    return f"{SWOW_NAMESPACE}:{quote(word)}"


def swow_node(*, word: str, response_counts: SwowResponseCounter) -> Node:
    """
    Create a cskg node from a SWOW cue or response.
    :param word: a SWOW cue or response
    :param response_counts: counts of responses to this word
    """
    return Node(
        datasource=SWOW_DATASOURCE_ID,
        id=swow_node_id(word),
        label=word,
        other={"response_counts": response_counts.counts},
    )


def swow_edge(
    *,
    cue: Union[Node, str],
    response: Union[Node, str],
    cue_response_counts: SwowResponseCounter,
    response_counts: SwowResponseCounter,
) -> Edge:
    """
    Create a cskg edge from a SWOW cue, response, and strength value.
    :param cue: cue phrase
    :param response: response to the cue phrase
    :param cue_response_counts: total response counts for the cue
    :param response_counts: counts of this response to the cue
    """
    cue_counts = cue_response_counts.counts
    resp_counts = response_counts.counts
    strength_r123 = sum(resp_counts.values()) / sum(cue_counts.values())
    other = {
        "response_counts": resp_counts,
        "response_strengths": {
            k: (resp_counts[k] / cue_counts[k] if cue_counts[k] > 0 else 0)
            for k in resp_counts.keys()
        },
    }
    return Edge(
        datasource=SWOW_DATASOURCE_ID,
        subject=cue if isinstance(cue, Node) else swow_node_id(cue),
        object_=response if isinstance(response, Node) else swow_node_id(response),
        predicate=RELATED_TO,
        weight=strength_r123,
        other=other,
    )
