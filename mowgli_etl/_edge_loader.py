from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.edge import Edge


class _EdgeLoader(_Loader):
    @abstractmethod
    def load_edge(self, edge: Edge):
        raise NotImplementedError
