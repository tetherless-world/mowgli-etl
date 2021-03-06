from typing import Optional, Generator

from mowgli_etl._closeable import _Closeable
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.storage._kg_node_set import _KgNodeSet


class MemKgNodeSet(_KgNodeSet, _Closeable):
    def __init__(self, **kwds):
        _KgNodeSet.__init__(self)
        _Closeable.__init__(self)
        self.__nodes = {}

    def add(self, node: KgNode) -> None:
        self.__nodes[node.id] = node

    def close(self):
        pass

    def delete(self, node_id: str) -> None:
        del self.__nodes[node_id]

    def get(self, node_id: str, default: Optional[KgNode] = None) -> Optional[KgNode]:
        return self.__nodes.get(node_id, default)

    def keys(self) -> Generator[str, None, None]:
        yield from self.__nodes.keys()

    @classmethod
    def temporary(cls):
        return cls()
