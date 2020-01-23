from abc import ABC

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._transformer import _Transformer


class _Pipeline(ABC):
    def __init__(self, *, extractor: _Extractor, transformer: _Transformer):
        self.__extractor = extractor
        self.__transformer = transformer
