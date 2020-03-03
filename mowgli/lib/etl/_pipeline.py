from abc import ABC
from typing import Optional

from configargparse import ArgParser

from mowgli.lib.etl._extractor import _Extractor
from mowgli.lib.etl._loader import _Loader
from mowgli.lib.etl._transformer import _Transformer
from mowgli.lib.etl.cskg.cskg_csv_loader import CskgCsvLoader
from mowgli.lib.etl.rdf.rdf_loader import RdfLoader


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
        self.__loader = self.__create_loader(id=id, **kwds)
        self.__transformer = transformer

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser) -> None:
        """
        Add pipeline-specific arguments. The parsed arguments are passed to the constructor as keywords.
        """
        cls.__add_loader_arguments(arg_parser)

    @classmethod
    def __add_loader_arguments(cls, arg_parser):
        arg_parser.add_argument("--loader", default="cskg_csv")

    def __create_loader(self, id: str, loader: Optional[str] = None, **loader_kwds) -> _Loader:
        if loader is None:
            loader = "cskg_csv"
        else:
            loader = loader.lower()

        if loader == "cskg_csv":
            return CskgCsvLoader()
        elif loader == "rdf":
            return RdfLoader(pipeline_id=id)  # Default format
        elif loader.startswith("rdf-"):
            return RdfLoader(format=loader[len("rdf-"):], pipeline_id=id)
        else:
            raise NotImplementedError(loader)

    @property
    def extractor(self):
        return self.__extractor

    @property
    def id(self):
        return self.__id

    @property
    def loader(self):
        return self.__loader

    @property
    def transformer(self):
        return self.__transformer
