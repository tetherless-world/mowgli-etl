import json
from typing import Optional, Dict, NamedTuple, Tuple


class KgEdge(NamedTuple):
    """
    Edge model. Edges are (subject, predicate, object) triples such as (hand, hasPart, finger).

    :param id: edge identifier, usually a concatenation of the subject, predicate and object
    :param object: object node id
    :param predicate: predicate id, should usually be a ConceptNet predicate (see concept_net_predicates.py)
    :param sources: one or more sources, the first must be the pipeline id (e.g., "swow")
    :param subject: subject node id
    :param labels: zero or more human-readable labels for the edge
    """

    id: str
    object: str
    predicate: str
    sources: Tuple[str, ...]
    subject: str
    labels: Optional[Tuple[str, ...]] = None

    @classmethod
    def legacy(cls, *, datasource: str, object: str, predicate: str, subject: str, other: Optional[Dict[str, object]] = None, weight: Optional[float] = None):
        return \
            cls.with_generated_id(
                object=object,
                labels=None,
                predicate=predicate,
                sources=(datasource,),
                subject=subject,
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
