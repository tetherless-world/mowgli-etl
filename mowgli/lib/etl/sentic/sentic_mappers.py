
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.sentic.sentic_constants import SENTIC_DATASOURCE_ID, SENTIC_NAMESPACE
from typing import Union
from urllib.parse import quote

def sentic_node(incominglabel: str) -> Node:

    return Node(
        datasource=SENTIC_DATASOURCE_ID,
        id=f'{SENTIC_NAMESPACE}:{quote(incominglabel)}',
        label=incominglabel
    )


def sentic_edge(*, subject: Union[Node, str], object_: Union[Node, str], weight: float = None,predicate = RELATED_TO) -> Edge:

    return Edge(
        datasource=SENTIC_DATASOURCE_ID,
        subject=subject if isinstance(subject, Node) else sentic_node(subject),
        object_=object_ if isinstance(object_, Node) else sentic_node(object_),
        predicate = predicate,
        weight = weight       
    )

