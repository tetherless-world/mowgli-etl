import pickle
from typing import Optional

from mowgli.lib.cskg.node import Node
from mowgli.lib.storage._leveldb import _Leveldb


class PersistentNodeSet(_Leveldb):
    def add(self, node: Node) -> None:
        key = self.__key(node_id=node.id)
        value = pickle.dumps(node)
        self._db.put(key, value)

    def get(self, *, node_id: str) -> Optional[Node]:
        key = self.__key(node_id=node_id)
        value = self._db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return None

    def __key(self, *, node_id: str) -> bytes:
        return node_id.encode("utf-8")
