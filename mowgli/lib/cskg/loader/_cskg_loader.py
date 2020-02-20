import logging
from abc import ABC, abstractmethod

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node

class _CskgLoader(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self._CskgWriter.__name__)

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
