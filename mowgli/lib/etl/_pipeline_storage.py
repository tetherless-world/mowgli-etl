from abc import ABC, abstractmethod
from io import IOBase
from typing import Union


class _PipelineStorage(ABC):
    @abstractmethod
    def get(self, key: str) -> IOBase:
        """
        Get a file-like object associated with the given key
        """

    @abstractmethod
    def head(self, key: str) -> bool:
        """
        Check if a value is associated with the given key
        """

    @abstractmethod
    def put(self, key: str, value: Union[bytearray, IOBase, str]) -> bool:
        """
        Put a file-like object or value associated with the given key
        :return true if there was a value previously associated with the key
        """
        pass
