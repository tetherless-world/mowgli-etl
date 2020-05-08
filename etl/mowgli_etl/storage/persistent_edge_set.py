import pickle
from typing import Optional

from mowgli_etl.lib.cskg.edge import Edge
from mowgli_etl.storage._edge_set import _EdgeSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentEdgeSet(_EdgeSet, LevelDb):
    def __init__(self, **kwds):
        _EdgeSet.__init__(self)
        LevelDb.__init__(self, **kwds)

    def add(self, edge: Edge) -> None:
        key = self.__construct_edge_key(object=edge.object, predicate=edge.predicate, subject=edge.subject)
        value = pickle.dumps(edge)
        self._db.put(key, value)

    def __construct_edge_key(self, *, object: str, predicate: str, subject: str) -> bytes:
        return self._construct_edge_key(object=object, predicate=predicate, subject=subject).encode("utf-8")

    def get(self, *, object: str, predicate: str, subject: str) -> Optional[Edge]:
        key = self.__construct_edge_key(object=object, predicate=predicate, subject=subject)
        value = self._db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return None
