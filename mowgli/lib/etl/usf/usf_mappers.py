from typing import Union

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.usf.usf_constants import USF_DATASOURCE_ID, USF_NAMESPACE


def usf_node(cueOrResponse: str, pos: str) -> Node:
    return Node(
        datasource=USF_DATASOURCE_ID,
        id=f'{USF_NAMESPACE}:{cueOrResponse.replace(" ", "_")}',
        label=cueOrResponse,
        pos=pos
    )


def usf_edge(*, cue: Union[Node, str], response: Union[Node, str], strength: float) -> Edge:

    return Edge(
        datasource=USF_DATASOURCE_ID,
        subject=cue if isinstance(cue, Node) else usf_node(cue, ""),
        object_=response if isinstance(response, Node) else usf_node(response, ""),
        predicate=RELATED_TO,
        weight=strength
    )
