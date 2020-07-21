from typing import Optional

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.storage._kg_edge_set import _KgEdgeSet


class MemKgEdgeSet(_KgEdgeSet):
    def __init__(self):
        _KgEdgeSet.__init__(self)
        self.__edges = {}

    def add(self, edge: KgEdge) -> None:
        self.__edges[edge.id] = edge

    def close(self):
        pass

    def get(self, edge_id: str, default: Optional[KgEdge] = None) -> Optional[KgEdge]:
        return self.__edges.get(edge_id, default)

    @classmethod
    def temporary(cls):
        return cls()
