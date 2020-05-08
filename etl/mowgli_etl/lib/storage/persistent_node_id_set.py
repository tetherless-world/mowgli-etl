from mowgli_etl.lib.storage._node_id_set import _NodeIdSet
from mowgli_etl.lib.storage.level_db import LevelDb


class PersistentNodeIdSet(_NodeIdSet, LevelDb):
    def __init__(self, **kwds):
        _NodeIdSet.__init__(self)
        LevelDb.__init__(self, **kwds)

    def add(self, node_id: str) -> None:
        key = self.__construct_node_key(node_id=node_id)
        value = b''
        self._db.put(key, value)

    @staticmethod
    def __construct_node_key(node_id: str) -> bytes:
        return node_id.encode("utf-8")

    def __contains__(self, node_id: str):
        key = self.__construct_node_key(node_id=node_id)
        value = self._db.get(key)
        return value is not None
