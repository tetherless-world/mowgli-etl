from typing import Optional, Tuple, Dict, NamedTuple


class Node(NamedTuple):
    id: str
    label: str
    aliases: Optional[Tuple[str, ...]] = None
    pos: Optional[str] = None
    # datasource is not optional, but it's ordered among the optional fields in the CSKG format
    datasource: str = ''
    other: Optional[Dict[str, object]] = None
