from abc import ABC, abstractmethod

from mowgli_etl._closeable import _Closeable


class _IdSet(_Closeable):
    @abstractmethod
    def add(self, id: str) -> None:
        """
        Add a id to the set.
        """

    @abstractmethod
    def __contains__(self, id: str) -> bool:
        """
        Test whether the given id is part of the set.
        """

    @classmethod
    @abstractmethod
    def temporary(cls):
        """
        Factory method to create a temporary id set.
        """
