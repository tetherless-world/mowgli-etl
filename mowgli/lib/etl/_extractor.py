import bz2
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict
from urllib.request import urlopen

from pathvalidate import sanitize_filename

from mowgli.lib.etl.pipeline_storage import PipelineStorage
from zipfile import ZipFile
import os.path
from io import BytesIO, TextIOBase

class _Extractor(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _download(self, from_url: str, force: bool, storage: PipelineStorage) -> None:
        """
        Utility method to download a file from a URL to a local file path.
        """

        downloaded_file_path = storage.extracted_data_dir_path / sanitize_filename(from_url)
        if not force and os.path.isfile(downloaded_file_path):
            self._logger.info(
                "%s already download and force not specified, skipping download",
                from_url)
            return

        self._logger.info("downloading %s", from_url)
        in_f = urlopen(from_url)
        with open(downloaded_file_path, "w+b") as out_f:
            out_f.write(in_f.read())
        self._logger.info("downloaded %s", from_url)

    @abstractmethod
    def extract(self, *, force: bool, storage: PipelineStorage) -> Optional[Dict[str, object]]:
        """
        Extract data from a source.
        :param force: force extraction, ignoring any cached data
        :return a **kwds dictionary to merge with kwds to pass to transformer
        """

    def _extract_bz2(self, path: str, force: bool, storage: PipelineStorage) -> None:
        """
        Utility method to decompress a local bz2 file and load it into the given storage repository.
        """

        extracted_file_path = storage.extracted_data_dir_path / sanitize_filename(path)
        if not force and storage.head(extracted_file_path):
            self._logger.info(
                "%s already extracted and force not specified, skipping decompression",
                path)
            return
        self._logger.info("extracting bz2 file %s", path)
        with bz2.open(path) as in_f:
            with open(extracted_file_path, "w+b") as out_f:
                out_f.write(in_f.read())
        self._logger.info("extracted bz2 file %s", path)

    def _extract_zip(self, from_url: str, force: bool, storage: PipelineStorage,target:str) -> str:
        """
        Utility method to decompress a local zip file and load it into the given storage repository.
        """

        zip_file_path = storage.extracted_data_dir_path / sanitize_filename(from_url)

        if not storage.head(zip_file_path):
            self._logger.info("%s zip not downloaded, try again", from_url)

        with open(zip_file_path, "rb") as extracted_file:
            with ZipFile(extracted_file) as ZipObj:
                self._logger.info("extracting zip folder %s", from_url)

                file = ZipObj.filelist[0]

                for f in ZipObj.filelist:
                  dirlist = f.filename.split("/")
                  if dirlist[-1] == target:
                      file = f
                      break


                """if not force and storage.head(file.filename):
                    self._logger.info("%s already zipped and force not specified, skipping extraction",file.filename)
                    return file.filename"""

                xmlobj = ZipObj.read(file.filename)

                extracted_file_path = storage.extracted_data_dir_path / file.filename
                with open(extracted_file_path, "w+b") as extracted_file:
                    extracted_file.write(xmlobj)

                return file.filename
