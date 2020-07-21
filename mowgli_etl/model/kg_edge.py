import json
from typing import Optional, Dict, NamedTuple, Tuple


class KgEdge(NamedTuple):
    id: str
    object: str
    predicate: str
    sources: Tuple[str, ...]
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
                sources=(datasource,),
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
