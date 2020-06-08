import logging
from abc import ABC, abstractmethod

from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.node import Node
from mowgli_etl.pipeline_storage import PipelineStorage


class _Loader(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def close(self) -> None:
        """
        Close this loader.
        """

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwds):
        self.close()

    @abstractmethod
    def open(self, storage: PipelineStorage):
        """
        Open this loader before calling load_* methods.
        """
        return self

    @abstractmethod
    def load_edge(self, edge: Edge):
        pass

    @abstractmethod
    def load_node(self, node: Node):
        pass
