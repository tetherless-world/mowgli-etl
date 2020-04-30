from collections import Counter
from enum import Enum, auto
from typing import Union
from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.swow.swow_constants import SWOW_DATASOURCE_ID, SWOW_NAMESPACE

""" 
Utility methods for mapping SWOW data into MOWGLI CSKG data structures.
"""


class SwowResponseType(Enum):
    R1 = auto()
    R2 = auto()
    R3 = auto()


def swow_node_id(word: str) -> str:
    return f"{SWOW_NAMESPACE}:{quote(word)}"


def swow_node(*, word: str, response_counts: Counter) -> Node:
    """
    Create a cskg node from a SWOW cue or response.
    :param word: a SWOW cue or response
    :param response_counts: counts of responses to this word
    """
    assert all(k in SwowResponseType.__members__ for k in response_counts.keys())
    return Node(
        datasource=SWOW_DATASOURCE_ID,
        id=swow_node_id(word),
        label=word,
        other={
            "response_counts": {
                rt: response_counts[rt] for rt in SwowResponseType.__members__.keys()
            }
        },
    )


def swow_edge(
    *,
    cue: Union[Node, str],
    response: Union[Node, str],
    cue_response_counts: Counter,
    response_counts: Counter,
) -> Edge:
    """
    Create a cskg edge from a SWOW cue, response, and strength value.
    :param cue: cue phrase
    :param response: response to the cue phrase
    :param cue_response_counts: total response counts for the cue
    :param response_counts: counts of this response to the cue
    """
    assert all(k in SwowResponseType.__members__ for k in cue_response_counts.keys())
    assert all(k in SwowResponseType.__members__ for k in response_counts.keys())
    strength_r123 = sum(response_counts.values()) / sum(cue_response_counts.values())
    other = {
        "response_counts": {
            rt: response_counts[rt] for rt in SwowResponseType.__members__.keys()
        },
        "response_strengths": {
            rt: (
                response_counts[rt] / cue_response_counts[rt]
                if cue_response_counts[rt] > 0
                else 0
            )
            for rt in SwowResponseType.__members__.keys()
        },
    }
    return Edge(
        datasource=SWOW_DATASOURCE_ID,
        subject=cue.id if isinstance(cue, Node) else swow_node_id(cue),
        object=response.id if isinstance(response, Node) else swow_node_id(response),
        predicate=RELATED_TO,
        weight=strength_r123,
        other=other,
    )
