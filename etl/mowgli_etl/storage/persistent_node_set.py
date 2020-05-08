import pickle
from typing import Optional, Generator

from mowgli_etl.lib.cskg.node import Node
from mowgli_etl.storage._node_set import _NodeSet
from mowgli_etl.storage.level_db import LevelDb


class PersistentNodeSet(_NodeSet, LevelDb):
    def __init__(self, **kwds):
        _NodeSet.__init__(self)
        LevelDb.__init__(self, **kwds)

    def add(self, node: Node) -> None:
        key = self.__construct_node_key(node.id)
        value = pickle.dumps(node)
        self._db.put(key, value)

    def delete(self, node_id: str) -> None:
        key = self.__construct_node_key(node_id)
        self._db.delete(key)

    @staticmethod
    def __construct_node_key(node_id: str) -> bytes:
        return node_id.encode("utf-8")

    def __contains__(self, node_id: str):
        key = self.__construct_node_key(node_id)
        value = self._db.get(key)
        return value is not None

    def get(self, node_id: str, default: Optional[Node] = None) -> Optional[Node]:
        key = self.__construct_node_key(node_id)
        value = self._db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return default

    def keys(self) -> Generator[str, None, None]:
        with self._db.iterator(include_value=False) as it:
            for key in it:
                yield key.decode("utf-8")
