import bz2
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict
from urllib.request import urlopen

from mowgli.lib.etl._pipeline_storage import _PipelineStorage


class _Extractor(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _download(self, from_url: str, force: bool, storage: _PipelineStorage) -> None:
        """
        Utility method to download a file from a URL to a local file path.
        """
        if not force and storage.head(from_url):
            self._logger.info(
                "%s already download and force not specified, skipping download",
                from_url)
            return

        self._logger.info("downloading %s to %s", from_url)
        f = urlopen(from_url)
        storage.put(from_url, f)
        self._logger.info("downloaded %s", from_url)

    @abstractmethod
    def extract(self, *, force: bool, storage: _PipelineStorage) -> Optional[Dict[str, object]]:
        """
        Extract data from a source.
        :param force: force extraction, ignoring any cached data
        :return a **kwds dictionary to merge with kwds to pass to transformer
        """

    def _extract_bz2(self, path: str, force: bool, storage: _PipelineStorage) -> None:
        """
        Utility method to decompress a local bz2 file and load it into the given storage repository.
        """
        if not force and storage.head(path):
            self._logger.info(
                "%s already extracted and force not specified, skipping decompression",
                path)
            return
        self._logger.info("extracting bz2 file %s", path)
        f = bz2.open(path)
        storage.put(path, f)
        self._logger.info("extracted bz2 file %s", path)
