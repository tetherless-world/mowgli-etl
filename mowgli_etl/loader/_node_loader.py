from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node


class _NodeLoader(_Loader):
    @abstractmethod
    def load_node(self, node: Node):
        raise NotImplementedError
