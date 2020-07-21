from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode


class _KgNodeLoader(_Loader):
    @abstractmethod
    def load_kg_node(self, node: KgNode):
        raise NotImplementedError
