from typing import Optional

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.storage._edge_set import _EdgeSet


class MemEdgeSet(_EdgeSet):
    def __init__(self):
        _EdgeSet.__init__(self)
        self.__edges = {}

    def add(self, edge: Edge) -> None:
        key = self._construct_edge_key(object_=edge.object, predicate=edge.predicate, subject=edge.subject)
        self.__edges[key] = edge

    def get(self, *, object_: str, predicate: str, subject: str) -> Optional[Edge]:
        key = self._construct_edge_key(object_=object_, predicate=predicate, subject=subject)
        return self.__edges.get(key)
