from typing import Optional

from mowgli_etl._closeable import _Closeable
from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.storage._edge_set import _EdgeSet


class MemEdgeSet(_EdgeSet, _Closeable):
    def __init__(self):
        _EdgeSet.__init__(self)
        _Closeable.__init__(self)
        self.__edges = {}

    def add(self, edge: Edge) -> None:
        key = self._construct_edge_key(object=edge.object, predicate=edge.predicate, subject=edge.subject)
        self.__edges[key] = edge

    def get(self, *, object: str, predicate: str, subject: str, default: Optional[Edge] = None) -> Optional[Edge]:
        key = self._construct_edge_key(object=object, predicate=predicate, subject=subject)
        return self.__edges.get(key, default)
