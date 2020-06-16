from abc import abstractmethod

from mowgli_etl._loader import _Loader
from mowgli_etl.model.path import Path


class _PathLoader(_Loader):
    @abstractmethod
    def load_path(self, path: Path):
        raise NotImplementedError
