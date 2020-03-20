
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.onto.onto_constants import ONTO_DATASOURCE_ID, ONTO_NAMESPACE
from typing import Union
from urllib.parse import quote

def onto_node(incominglabel: str) -> Node:

    return Node(
        datasource=ONTO_DATASOURCE_ID,
        id=f'{ONTO_NAMESPACE}:{quote(incominglabel)}',
        label=incominglabel
    )


def onto_edge(*, subject: Union[Node, str], object_: Union[Node, str]) -> Edge:

    return Edge(
        datasource=ONTO_DATASOURCE_ID,
        subject=subject if isinstance(subject, Node) else onto_node(subject),
        object_=object_ if isinstance(object_, Node) else onto_node(object_),
        predicate = None
    )

