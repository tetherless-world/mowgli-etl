from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.kg_edge import KgEdge


class _EdgeLoader(_Loader):
    @abstractmethod
    def load_edge(self, edge: KgEdge):
        raise NotImplementedError
