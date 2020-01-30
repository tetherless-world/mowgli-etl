from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge

""" 
Utility methods for mapping SWOW data into MOWGLI CSKG data structures.
"""

def swow_node(cueOrResponse: str) -> Node:
    """ 
    Create a cskg node from a SWOW cue or response.
    :param cueOrResponse: a SWOW cue or response
    """
    return Node(
        datasource='swow',
        id=f'swow:{cueOrResponse.replace(" ", "_")}',
        label=cueOrResponse
    )

def swow_edge(*, cue: str, response: str, strength: float) -> Edge:
    """
    Create a cskg edge from a SWOW cue, response, and strength value.
    :param cue: cue phrase
    :param response: response to the cue phrase
    :param strength: frequency of the response among all responses for the cue word
    """ 
    return Edge(
        datasource='swow',
        subject=swow_node(cue),
        object_=swow_node(response),
        relation='/r/RelatedTo',
        weight=strength
    )
