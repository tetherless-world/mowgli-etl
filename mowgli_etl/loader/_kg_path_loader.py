from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.kg_path import KgPath


class _KgPathLoader(_Loader):
    @abstractmethod
    def load_kg_path(self, path: KgPath):
        raise NotImplementedError
