from typing import Optional, Dict, NamedTuple


class Edge(NamedTuple):
    datasource: str
    object: str
    predicate: str
    subject: str
    other: Optional[Dict[str, object]] = None
    weight: Optional[float] = None
