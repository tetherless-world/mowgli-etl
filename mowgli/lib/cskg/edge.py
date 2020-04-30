from typing import Optional, Dict, NamedTuple


class Edge(NamedTuple):
    subject: str
    predicate: str
    object: str
    datasource: str
    weight: Optional[float] = None
    other: Optional[Dict[str, object]] = None
