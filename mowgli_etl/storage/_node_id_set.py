from abc import ABC, abstractmethod

from mowgli_etl._closeable import _Closeable


class _NodeIdSet(_Closeable):
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

    @classmethod
    @abstractmethod
    def temporary(cls):
        """
        Factory method to create a temporary node id set.
        """
