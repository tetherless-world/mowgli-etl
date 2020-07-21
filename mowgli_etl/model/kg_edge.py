import json
from typing import Optional, Dict, NamedTuple


class KgEdge(NamedTuple):
    subject: str
    predicate: str
    object: str
    datasource: str
    weight: Optional[float] = None
    other: Optional[Dict[str, object]] = None

    @classmethod
    def legacy(cls, *, datasource: str, object: str, predicate: str, subject: str, other: Optional[Dict[str, object]] = None, weight: Optional[float] = None):
        return \
            cls(
                datasource=datasource,
                object=object,
                other=other,
                predicate=predicate,
                subject=subject,
                weight=weight
            )

    def __hash__(self):
        return hash((
            self.datasource,
            self.object,
            json.dumps(self.other, sort_keys=True),
            self.predicate,
            self.subject,
            self.weight
        ))
