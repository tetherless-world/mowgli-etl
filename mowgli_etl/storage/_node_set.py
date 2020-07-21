from abc import ABC, abstractmethod
from typing import Optional, Generator

from mowgli_etl._closeable import _Closeable
from mowgli_etl.model.kg_node import KgNode


class _NodeSet(_Closeable):
    def add(self, node: KgNode) -> None:
        """
        Add a node to the set.
        """

    def __contains__(self, node_id):
        return self.get(node_id) is not None

    @abstractmethod
    def delete(self, node_id: str) -> None:
        """
        Delete a node from the set by id.
        """

    @abstractmethod
    def get(self, node_id: str, default: Optional[KgNode] = None) -> Optional[KgNode]:
        """
        Get a node by id from the set.
        :return: the node corresponding to the id if the former is in the set, otherwise None
        """

    @abstractmethod
    def keys(self) -> Generator[str, None, None]:
        """
        Iterate over the node id's in the set as a generator.
        """

    @classmethod
    @abstractmethod
    def temporary(cls):
        """
        Factory method to create a temporary node set.
        """
