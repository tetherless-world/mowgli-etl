from abc import ABC

from configargparse import ArgParser

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._transformer import _Transformer


class _Pipeline(ABC):
    def __init__(self, *, extractor: _Extractor, id: str, transformer: _Transformer, **kwds):
        """
        Construct an extract-transform pipeline.
        :param extractor: extractor implementation
        :param id: unique identifier for this pipeline instance, may be adapted from arguments
        :param transformer: transformer implementation
        :param kwds: ignored
        """
        self.__extractor = extractor
        self.__id = id
        self.__transformer = transformer

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        """
        Add pipeline-specific arguments. The parsed arguments are passed to the constructor as keywords.
        """

    @property
    def extractor(self):
        return self.__extractor

    @property
    def id(self):
        return self.__id

    @property
    def transformer(self):
        return self.__transformer
