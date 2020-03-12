
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.onto.onto_constants import ONTO_DATASOURCE_ID, ONTO_NAMESPACE
from typing import Union

def onto_node(cueOrResponse: str) -> Node:

    return Node(
        datasource=ONTO_DATASOURCE_ID,
        id=f'{ONTO_NAMESPACE}:{cueOrResponse.replace(" ", "_")}',
        label=cueOrResponse
    )


def onto_edge(*, cue: Union[Node, str], response: Union[Node, str]) -> Edge:

    return Edge(
        datasource=ONTO_DATASOURCE_ID,
        subject=cue if isinstance(cue, Node) else onto_node(cue),
        object_=response if isinstance(response, Node) else onto_node(response),
        predicate = None
    )

