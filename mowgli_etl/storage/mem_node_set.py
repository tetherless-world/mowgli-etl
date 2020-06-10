from typing import Optional, Generator

from mowgli_etl._closeable import _Closeable
from mowgli_etl.model.node import Node
from mowgli_etl.storage._node_set import _NodeSet


class MemNodeSet(_NodeSet, _Closeable):
    def __init__(self, **kwds):
        _NodeSet.__init__(self)
        _Closeable.__init__(self)
        self.__nodes = {}

    def add(self, node: Node) -> None:
        self.__nodes[node.id] = node

    def delete(self, node_id: str) -> None:
        del self.__nodes[node_id]

    def get(self, node_id: str, default: Optional[Node] = None) -> Optional[Node]:
        return self.__nodes.get(node_id, default)

    def keys(self) -> Generator[str, None, None]:
        yield from self.__nodes.keys()
