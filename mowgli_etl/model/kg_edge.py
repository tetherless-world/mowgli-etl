import json
from typing import Optional, Dict, NamedTuple, Tuple


class KgEdge(NamedTuple):
    """
    Edge model. Edges are (subject, predicate, object) triples such as (hand, hasPart, finger).

    :param id: edge identifier, usually a concatenation of the subject, predicate and object
    :param object: object node id
    :param predicate: predicate id, should usually be a ConceptNet predicate (see concept_net_predicates.py)
    :param source_ids: one or more source identifiers, the first must be the pipeline id (e.g., "swow")
    :param subject: subject node id
    :param labels: zero or more human-readable labels for the edge
    :param weight: deprecated, do not use
    """

    id: str
    object: str
    predicate: str
    source_ids: Tuple[str, ...]
    subject: str
    labels: Optional[Tuple[str, ...]] = None
    weight: Optional[float] = None

    @classmethod
    def legacy(cls, *, datasource: str, object: str, predicate: str, subject: str, other: Optional[Dict[str, object]] = None, weight: Optional[float] = None):
        return \
            cls.with_generated_id(
                object=object,
                labels=None,
                predicate=predicate,
                source_ids=(datasource,),
                subject=subject,
                weight=weight
            )

    @classmethod
    def with_generated_id(cls, object: str, predicate: str, subject: str, **kwds):
        return \
            cls(
                id=f"{subject}-{predicate}-{object}",
                object=object,
                predicate=predicate,
                subject=subject,
                **kwds
            )
