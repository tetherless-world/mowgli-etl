import pickle
from typing import Optional

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.storage._leveldb import _Leveldb


class PersistentEdgeSet(_Leveldb):
    def add(self, edge: Edge) -> None:
        key = self.__key(object_=edge.object, predicate=edge.predicate, subject=edge.subject)
        value = pickle.dumps(edge)
        self._db.put(key, value)

    def get(self, *, object_: str, predicate: str, subject: str) -> Optional[Edge]:
        key = self.__key(object_=object_, predicate=predicate, subject=subject)
        value = self._db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return None

    def __key(self, *, object_: str, predicate: str, subject: str) -> bytes:
        return f"{subject}\t{predicate}\t{object_}".encode("utf-8")
