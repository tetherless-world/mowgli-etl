import pickle
from typing import Optional, Generator

from mowgli.lib.cskg.node import Node
from mowgli.lib.storage._leveldb import _Leveldb
from mowgli.lib.storage._node_set import _NodeSet


class PersistentNodeSet(_NodeSet, _Leveldb):
    def __init__(self, **kwds):
        _NodeSet.__init__(self)
        _Leveldb.__init__(self, **kwds)

    def add(self, node: Node) -> None:
        key = self.__construct_node_key(node.id)
        value = pickle.dumps(node)
        self._db.put(key, value)

    @staticmethod
    def __construct_node_key(node_id: str) -> bytes:
        return node_id.encode("utf-8")

    def get(self, node_id: str) -> Optional[Node]:
        key = self.__construct_node_key(node_id)
        value = self._db.get(key)
        if value is not None:
            return pickle.loads(value)
        else:
            return None

    def keys(self) -> Generator[str, None, None]:
        with self._db.iterator() as it:
            for key, _ in it:
                yield key.decode("utf-8")
