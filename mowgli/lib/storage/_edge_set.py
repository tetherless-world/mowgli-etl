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

    @abstractmethod
    def get(self, *, object_: str, predicate: str, subject: str) -> Optional[Edge]:
        """
        Get an edge by its "signature" parameters.
        :return: the edge if it's part of the set, otherwise None
        """
