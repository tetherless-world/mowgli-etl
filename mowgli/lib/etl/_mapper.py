from abc import ABC, abstractmethod
from collections import Generator

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node


class _Mapper(ABC):
    @abstractmethod
    def map(self, node: Node) -> Generator[Edge, None, None]:
        """
        Given a node from a data source, generate a sequence of edges mapping that node to nodes in other data sources.
        """
