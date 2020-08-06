import bz2
import logging
import os.path
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Tuple, Union
from zipfile import ZipFile

from pathvalidate import sanitize_filename

from mowgli_etl.http_client.etl_http_client import EtlHttpClient
from mowgli_etl.http_client.real_etl_http_client import RealEtlHttpClient
from mowgli_etl.pipeline_storage import PipelineStorage


class _Extractor(ABC):
    """
    Abstract base class for extractors.

    See the extract method.
    """

    def __init__(self, http_client: EtlHttpClient = None, **kwargs):
        if http_client is None:
            http_client = RealEtlHttpClient()
        self.__http_client = http_client
        self._logger = logging.getLogger(self.__class__.__name__)

    def _download(self, from_url: str, force: bool, storage: PipelineStorage) -> Path:
        """
        Utility method to download a file from a URL to a local file path.
        """

        downloaded_file_path = storage.extracted_data_dir_path / sanitize_filename(
            from_url
        )
        if not force and os.path.isfile(downloaded_file_path):
            self._logger.info(
                "%s already download and force not specified, skipping download",
                from_url,
            )
        else:
            self._logger.info("downloading %s", from_url)
            in_f = self.__http_client.urlopen(from_url)
            with open(downloaded_file_path, "w+b") as out_f:
                out_f.write(in_f.read())
            self._logger.info("downloaded %s", from_url)
        return downloaded_file_path

    @abstractmethod
    def extract(
        self, *, force: bool, storage: PipelineStorage
    ) -> Optional[Dict[str, object]]:
        """
        Extract data from a source. The source data is passed to the transformer.
        :param force: force extraction, ignoring any cached data
        :return a **kwds dictionary to merge with kwds to pass to transformer
        """

    def _extract_bz2(self, path: str, force: bool, storage: PipelineStorage) -> Path:
        """
        Utility method to decompress a local bz2 file and load it into the given storage repository.
        """

        extracted_file_path = storage.extracted_data_dir_path / sanitize_filename(path)
        if not force and os.path.isfile(extracted_file_path):
            self._logger.info(
                "%s already extracted and force not specified, skipping decompression",
                path,
            )
            return extracted_file_path
        self._logger.info("extracting bz2 file %s", path)
        with bz2.open(path) as in_f:
            with open(extracted_file_path, "w+b") as out_f:
                out_f.write(in_f.read())
        self._logger.info("extracted bz2 file %s", path)
        return extracted_file_path

    def _extract_zip(
        self,
        *,
        archive_path: Union[str, Path],
        filenames: Union[str, Tuple[str, ...]],
        force: bool,
        storage: PipelineStorage
    ) -> Dict[str, Path]:
        """
        Decompress a local zip file and load it into the given storage.
        :param archive_path: path to zip archive
        :param force: if false, extraction will be skipped for files already present in storage
        :param storage: PipelineStorage instance
        :param filenames: name or tuple of names of files to extract from the archive
        :return paths to extracted filenames with order corresponding to filenames param.
        """
        extracted_dir = storage.extracted_data_dir_path
        if not isinstance(filenames, Tuple):
            filenames = (filenames,)
        extracted_file_paths = {fn: extracted_dir / fn for fn in filenames}
        if not force and all(fp.exists() for fp in extracted_file_paths.values()):
            self._logger.info(
                "%s already extracted from %s and force not specified.  Skipping extraction.",
                filenames,
                archive_path,
            )
        else:
            self._logger.info(
                "extracting %s from zip archive %s", filenames, archive_path
            )
            with ZipFile(archive_path) as zip_file:
                zip_file.extractall(path=extracted_dir, members=filenames)
        return extracted_file_paths
