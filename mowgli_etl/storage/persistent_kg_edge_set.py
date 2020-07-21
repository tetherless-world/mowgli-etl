import pickle
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.storage._kg_edge_set import _KgEdgeSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentKgEdgeSet(_KgEdgeSet):
    def __init__(self, **level_db_kwds):
        _KgEdgeSet.__init__(self)
        self.__level_db = LevelDb(**level_db_kwds)

    def add(self, edge: KgEdge) -> None:
        value = pickle.dumps(edge)
        self.__level_db.put(edge.id.encode("utf-8"), value)

    def close(self):
        self.__level_db.close()

    @property
    def closed(self):
        return self.__level_db.closed

    def get(self, edge_id, default: Optional[KgEdge] = None) -> Optional[KgEdge]:
        value = self.__level_db.get(edge_id.encode("utf-8"))
        if value is not None:
            return pickle.loads(value)
        else:
            return default

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
