from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.concept_net_predicates import HAS_A, MADE_OF
from mowgli.lib.etl.webchild.webchild_constants import WEBCHILD_MEMEBEROF_DATASOURCE_ID, WEBCHILD_PHYSICAL_DATASOURCE_ID, WEBCHILD_SUBSTANCEOF_DATASOURCE_ID, WEBCHILD_NAMESPACE
from typing import Union

""" 
Utility methods for mapping webchild data into MOWGLI CSKG data structures.
"""

def findProperDataSourceId(csvPath:str) -> str:
    if('partof_memberof' in csvPath):
        return WEBCHILD_MEMEBEROF_DATASOURCE_ID,HAS_A
    if('partof_physical' in csvPath):
        return WEBCHILD_PHYSICAL_DATASOURCE_ID,HAS_A
    if('partof_substanceof' in csvPath):
        return WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,MADE_OF

def webchild_node(cueOrResponse: str,*args, **kwargs) -> Node:
    """ 
    Create a cskg node from a webchild cue or response.
    :param cueOrResponse: a webchild cue or response
    """ 
    if('.txt' in args[0]):
        ds = findProperDataSourceId(args[0])[0]
    else:
        ds = args[0]
    return Node(
        datasource=ds,
        id=f'{WEBCHILD_NAMESPACE}:{cueOrResponse.replace(" ", "_")}',
        label=cueOrResponse
    )

def webchild_edge(*, cue: Union[Node, str], response: Union[Node, str], csvPath:str) -> Edge: #strength: float
    """
    Create a cskg edge from a webchild cue, response, and strength value.
    :param cue: cue phrase
    :param response: response to the cue phrase
    :param strength: frequency of the response among all responses for the cue word
    """ 
    ds,r = findProperDataSourceId(csvPath)
    return Edge(
        datasource=ds,
        subject=cue if isinstance(cue, Node) else webchild_node(cue,ds),
        object_=response if isinstance(response, Node) else webchild_node(response,ds),
        relation=r,
        #weight=strength
    )
