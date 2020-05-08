from abc import ABC, abstractmethod
from typing import Optional

from mowgli.lib.cskg.edge import Edge


class _EdgeSet(ABC):
    """
    Abstract base class for edge set data structure implementations.
    """

    @abstractmethod
    def add(self, edge: Edge) -> None:
        """
        Add an edge to the set.
        """

    def _construct_edge_key(self, *, object: str, predicate: str, subject: str) -> str:
        return f"{subject}\t{predicate}\t{object}"

    @abstractmethod
    def get(self, *, object: str, predicate: str, subject: str, default: Optional[Edge] = None) -> Optional[Edge]:
        """
        Get an edge by its "signature" parameters.
        :return: the edge if it's part of the set, otherwise None
        """
