from abc import ABC, abstractmethod
from typing import Optional

from mowgli_etl._closeable import _Closeable
from mowgli_etl.model.kg_edge import KgEdge


class _KgEdgeSet(_Closeable):
    """
    Abstract base class for edge set data structure implementations.
    """

    @abstractmethod
    def add(self, edge: KgEdge) -> None:
        """
        Add an edge to the set.
        """

    def __contains__(self, edge: KgEdge) -> bool:
        return self.get(id=edge.id) is not None

    @abstractmethod
    def get(self, edge_id: str, default: Optional[KgEdge] = None) -> Optional[KgEdge]:
        """
        Get an edge by id.
        :return: the edge if it's part of the set, otherwise None
        """

    @classmethod
    @abstractmethod
    def temporary(cls):
        """
        Factory method to create a temporary edge set.
        """
