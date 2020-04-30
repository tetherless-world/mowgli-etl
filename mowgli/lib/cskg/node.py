from typing import Optional, Tuple, Dict, NamedTuple


class Node(NamedTuple):
    datasource: str
    id: str
    label: str
    aliases: Optional[Tuple[str, ...]] = None
    other: Optional[Dict[str, object]] = None
    pos: Optional[str] = None
