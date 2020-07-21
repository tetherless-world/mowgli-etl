from typing import Optional, Union
from urllib.parse import quote

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.sentic.sentic_constants import (
    SENTIC_DATASOURCE_ID,
    SENTIC_NAMESPACE, SENTIC_TYPE_KEY,
)


def sentic_id(id: str, type: str) -> str:
    return f"{SENTIC_NAMESPACE}:{type}:{quote(id)}"


def sentic_node(*, id: str, label: str = None, sentic_type: str) -> KgNode:
    if label is None:
        label = id
    return KgNode.legacy(
        datasource=SENTIC_DATASOURCE_ID,
        id=sentic_id(id, sentic_type),
        label=label,
        other={SENTIC_TYPE_KEY: sentic_type},
    )


def sentic_edge(
    *,
    subject: str,
    object_: str,
    weight: Optional[float] = None,
) -> KgEdge:

    return KgEdge.legacy(
        datasource=SENTIC_DATASOURCE_ID,
        subject=subject,
        object=object_,
        predicate=RELATED_TO,
        weight=weight,
    )
