from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.kg_path import KgPath


class _PathLoader(_Loader):
    @abstractmethod
    def load_path(self, path: KgPath):
        raise NotImplementedError
