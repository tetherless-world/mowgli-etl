import logging
from abc import ABC, abstractmethod

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node

class _Loader(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *args, **kwds):
        pass

    @classmethod
    @abstractmethod
    def mime_type(cls) -> str:
        pass

    @abstractmethod
    def load_edge(self, edge: Edge):
        pass

    @abstractmethod
    def load_node(self, node: Node):
        pass
