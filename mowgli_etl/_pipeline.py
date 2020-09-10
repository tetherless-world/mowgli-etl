from abc import ABC
from typing import Optional, Union

from configargparse import ArgParser

from mowgli_etl._extractor import _Extractor
from mowgli_etl._loader import _Loader
from mowgli_etl._transformer import _Transformer
from mowgli_etl.loader.cskg_csv.cskg_csv_loader import CskgCsvLoader
from mowgli_etl.loader.kgtk.kgtk_edges_tsv_loader import KgtkEdgesTsvLoader


class _Pipeline(ABC):
    """
    Abstract base class for extract-transform-load pipelines.

    A pipeline consists of an extractor, a transformer, and a loader. Most pipeline implementations (subclasses) only supply the former two.
    """

    def __init__(self, *, extractor: _Extractor, id: str, transformer: _Transformer, loader: Optional[Union[_Loader, str]] = None, single_source=True, **kwds):
        """
        Construct an extract-transform-load pipeline.
        :param extractor: extractor implementation
        :param id: unique identifier for this pipeline instance, may be adapted from arguments
        :param loader: optional _Loader instance or loader name to use
        :param single_source: indicates whether the pipeline emits a single source (per the sources fields in nodes and edges)
        :param transformer: transformer implementation
        :param kwds: ignored
        """
        self.__extractor = extractor
        self.__id = id
        if not isinstance(loader, _Loader):
            loader = self.__create_loader(id=id, loader=loader, **kwds)
        self.__loader = loader
        self.__single_source = single_source
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
        elif loader == "kgtk_edges_tsv":
            return KgtkEdgesTsvLoader()
        else:
            raise NotImplementedError(loader)

    @property
    def extractor(self) -> _Extractor:
        return self.__extractor

    @property
    def id(self) -> str:
        return self.__id

    @property
    def loader(self) -> _Loader:
        return self.__loader

    @property
    def single_source(self) -> bool:
        return self.__single_source

    @property
    def transformer(self) -> _Transformer:
        return self.__transformer
