import json
from typing import Optional, Tuple, Dict, NamedTuple


class KgNode(NamedTuple):
    id: str
    label: str
    aliases: Optional[Tuple[str, ...]] = None
    pos: Optional[str] = None
    # datasource is not optional, but it's ordered among the optional fields in the CSKG format
    datasource: str = ''
    other: Optional[Dict[str, object]] = None

    @classmethod
    def legacy(cls, *, datasource: str, id: str, label: str, aliases: Optional[Tuple[str, ...]] = None, pos: Optional[str] = None, other: Optional[Dict[str, object]] = None):
        return \
            cls(
                aliases=aliases,
                datasource=datasource,
                id=id,
                other=other,
                pos=pos,
                label=label,
            )

    def __hash__(self):
        return hash((
            self.aliases,
            self.datasource,
            self.id,
            self.label,
            json.dumps(self.other, sort_keys=True),
            self.pos
        ))
