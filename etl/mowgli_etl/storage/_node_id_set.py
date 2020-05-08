from abc import ABC, abstractmethod


class _NodeIdSet(ABC):
    @abstractmethod
    def add(self, node_id: str) -> None:
        """
        Add a node id to the set.
        """

    @abstractmethod
    def __contains__(self, node_id: str) -> bool:
        """
        Test whether the given node id is part of the set.
        """
