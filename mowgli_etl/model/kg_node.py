import json
from typing import Optional, Tuple, Dict, NamedTuple


class KgNode(NamedTuple):
    """
    Node model.

    :param id: node id, should be an identifier with a namespace prefix such as "swow:word", where the prefix "swow" is the same as the pipeline id
    :param labels: one or more human-readable label
    :param source_ids: one or more source identifiers for this node, must start with the pipeline id (e.g., "swow")
    :param pos: part of speech: "n", "v", "r"
    """

    id: str
    labels: Tuple[str, ...]
    source_ids: Tuple[str, ...]
    pos: Optional[str] = None

    @classmethod
    def legacy(cls, *, datasource: str, id: str, label: str, aliases: Optional[Tuple[str, ...]] = None, pos: Optional[str] = None, other: Optional[Dict[str, object]] = None):
        return \
            cls(
                id=id,
                labels=((label,) if aliases is None else tuple([label] + list(aliases))),
                pos=pos,
                source_ids=(datasource,),
            )
