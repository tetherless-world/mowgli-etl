from typing import Optional, Union
from urllib.parse import quote

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.pipeline.sentic.sentic_constants import (
    SENTIC_DATASOURCE_ID,
    SENTIC_NAMESPACE,
)


def sentic_node(incominglabel: str, other: Optional[dict] = None) -> Node:
    # assert not incominglabel.startswith(SENTIC_NAMESPACE + ":")
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
        subject=subject.id if isinstance(subject, Node) else sentic_node(subject).id,
        object=object_.id if isinstance(object_, Node) else sentic_node(object_).id,
        predicate=predicate,
        weight=weight,
    )
