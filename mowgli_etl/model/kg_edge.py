import json
from typing import Optional, Dict, NamedTuple


class KgEdge(NamedTuple):
    subject: str
    predicate: str
    object: str
    datasource: str
    weight: Optional[float] = None
    other: Optional[Dict[str, object]] = None

    def __hash__(self):
        return hash((
            self.datasource,
            self.object,
            json.dumps(self.other, sort_keys=True),
            self.predicate,
            self.subject,
            self.weight
        ))
