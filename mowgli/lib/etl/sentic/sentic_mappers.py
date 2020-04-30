from typing import Optional, Union
from urllib.parse import quote

from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.sentic.sentic_constants import (
    SENTIC_DATASOURCE_ID,
    SENTIC_NAMESPACE,
)


def sentic_node(incominglabel: str, other: Optional[dict] = None) -> Node:
    return Node(
        datasource=SENTIC_DATASOURCE_ID,
        id=f"{SENTIC_NAMESPACE}:{quote(incominglabel)}",
        label=incominglabel,
        other=other,
    )


def sentic_edge(
    *,
    subject: Union[Node, str],
    object_: Union[Node, str],
    weight: float = None,
    predicate=RELATED_TO,
) -> Edge:

    return Edge(
        datasource=SENTIC_DATASOURCE_ID,
        subject=subject.id if isinstance(subject, Node) else sentic_node(subject),
        object=object_.id if isinstance(object_, Node) else sentic_node(object_),
        predicate=predicate,
        weight=weight,
    )
