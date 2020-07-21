from typing import Union
from urllib.parse import quote

from mowgli_etl.model.concept_net_predicates import RELATED_TO
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.pipeline.usf.usf_constants import USF_DATASOURCE_ID, USF_NAMESPACE


def usf_node(cueOrResponse: str, pos: str, other: dict = {}) -> KgNode:
    return KgNode(
        datasource=USF_DATASOURCE_ID,
        id=f'{USF_NAMESPACE}:{quote("%(cueOrResponse)s-%(pos)s" % locals())}',
        label=cueOrResponse,
        pos=pos,
        other= None if len(other) == 0 else other
    )


def usf_edge(*, cue: Union[KgNode, str], response: Union[KgNode, str], strength: float) -> KgEdge:

    return KgEdge(
        datasource=USF_DATASOURCE_ID,
        subject=cue.id if isinstance(cue, KgNode) else usf_node(cue, "", ),
        object=response.id if isinstance(response, KgNode) else usf_node(response, ""),
        predicate=RELATED_TO,
        weight=strength
    )
