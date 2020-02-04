import logging
from abc import ABC, abstractmethod
from typing import Generator, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node


class _Transformer(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def transform(self, **kwds) -> Generator[Union[Node, Edge], None, None]:
        """
        Transform previously-extracted data.
        :param kwds: merged dictionary of initial extract kwds and the result of extract
        :return: generator of nodes and edges
        """
