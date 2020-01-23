from abc import ABC, abstractmethod
from typing import Generator, Union

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node


class _Transformer(ABC):
    @abstractmethod
    def transform(self) -> Generator[Union[Node, Edge], None, None]:
        pass
