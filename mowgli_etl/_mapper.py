from abc import ABC, abstractmethod
from typing import Generator

from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


class _Mapper(ABC):
    @abstractmethod
    def map(self, node: KgNode) -> Generator[KgEdge, None, None]:
        """
        Given a node from a data source, generate a sequence of edges mapping that node to nodes in other data sources.
        """
