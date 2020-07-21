import pickle
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.storage._edge_set import _EdgeSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentEdgeSet(_EdgeSet):
    def __init__(self, **level_db_kwds):
        _EdgeSet.__init__(self)
        self.__level_db = LevelDb(**level_db_kwds)

    def add(self, edge: KgEdge) -> None:
        key = self.__construct_edge_key(object=edge.object, predicate=edge.predicate, subject=edge.subject)
        value = pickle.dumps(edge)
        self.__level_db.put(key, value)

    def close(self):
        self.__level_db.close()

    @property
    def closed(self):
        return self.__level_db.closed

    def __construct_edge_key(self, *, object: str, predicate: str, subject: str) -> bytes:
        return self._construct_edge_key(object=object, predicate=predicate, subject=subject).encode("utf-8")

    def get(self, *, object: str, predicate: str, subject: str) -> Optional[KgEdge]:
        key = self.__construct_edge_key(object=object, predicate=predicate, subject=subject)
        value = self.__level_db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return None

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
