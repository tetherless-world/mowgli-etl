from typing import Union
from urllib.parse import quote

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.pipeline.usf.usf_constants import USF_DATASOURCE_ID, USF_NAMESPACE


def usf_node(cueOrResponse: str, pos: str, other: dict = {}) -> Node:
    return Node(
        datasource=USF_DATASOURCE_ID,
        id=f'{USF_NAMESPACE}:{quote("%(cueOrResponse)s-%(pos)s" % locals())}',
        label=cueOrResponse,
        pos=pos,
        other= None if len(other) == 0 else other
    )


def usf_edge(*, cue: Union[Node, str], response: Union[Node, str], strength: float) -> Edge:

    return Edge(
        datasource=USF_DATASOURCE_ID,
        subject=cue.id if isinstance(cue, Node) else usf_node(cue, "", ),
        object=response.id if isinstance(response, Node) else usf_node(response, ""),
        predicate=RELATED_TO,
        weight=strength
    )
