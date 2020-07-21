import json
from typing import Optional, Tuple, Dict, NamedTuple


class KgNode(NamedTuple):
    id: str
    labels: Tuple[str, ...]
    sources: Tuple[str, ...]
    pos: Optional[str] = None

    @classmethod
    def legacy(cls, *, datasource: str, id: str, label: str, aliases: Optional[Tuple[str, ...]] = None, pos: Optional[str] = None, other: Optional[Dict[str, object]] = None):
        return \
            cls(
                id=id,
                labels=((label,) if aliases is None else tuple([label] + list(aliases))),
                pos=pos,
                sources=(datasource,),
            )
