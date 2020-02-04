from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.swow.swow_constants import SWOW_DATASOURCE_ID, SWOW_NAMESPACE
from typing import Union

""" 
Utility methods for mapping SWOW data into MOWGLI CSKG data structures.
"""

def swow_node(cueOrResponse: str) -> Node:
    """ 
    Create a cskg node from a SWOW cue or response.
    :param cueOrResponse: a SWOW cue or response
    """
    return Node(
        datasource=SWOW_DATASOURCE_ID,
        id=f'{SWOW_NAMESPACE}:{cueOrResponse.replace(" ", "_")}',
        label=cueOrResponse
    )

def swow_edge(*, cue: Union[Node, str], response: Union[Node, str], strength: float) -> Edge:
    """
    Create a cskg edge from a SWOW cue, response, and strength value.
    :param cue: cue phrase
    :param response: response to the cue phrase
    :param strength: frequency of the response among all responses for the cue word
    """ 
    return Edge(
        datasource=SWOW_DATASOURCE_ID,
        subject=cue if isinstance(cue, Node) else swow_node(cue),
        object_=response if isinstance(response, Node) else swow_node(response),
        relation=RELATED_TO,
        weight=strength
    )
