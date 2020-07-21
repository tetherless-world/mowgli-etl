from pathlib import Path
from tempfile import mkdtemp

from mowgli_etl.storage._node_id_set import _NodeIdSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentNodeIdSet(_NodeIdSet):
    def __init__(self, **level_db_kwds):
        _NodeIdSet.__init__(self)
        self.__level_db = LevelDb(**level_db_kwds)

    def add(self, node_id: str) -> None:
        key = self.__construct_node_key(node_id=node_id)
        value = b''
        self.__level_db.put(key, value)

    def close(self):
        self.__level_db.close()

    @property
    def closed(self):
        return self.__level_db.closed

    @staticmethod
    def __construct_node_key(node_id: str) -> bytes:
        return node_id.encode("utf-8")

    def __contains__(self, node_id: str):
        key = self.__construct_node_key(node_id=node_id)
        value = self.__level_db.get(key)
        return value is not None

    @classmethod
    def temporary(cls):
        return cls(directory_path=Path(mkdtemp()), delete_on_close=True)
