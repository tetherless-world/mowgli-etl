import os.path
from io import TextIOWrapper
from zipfile import ZipFile

from mowgli import paths


class CskgReleaseArchive:
    def __init__(self):
        extracted_data_dir_path = paths.DATA_DIR / "cskg_release" / "extracted"
        for extracted_file_name in os.listdir(extracted_data_dir_path):
            if os.path.splitext(extracted_file_name)[1] != ".zip":
                continue
            extracted_file_path = extracted_data_dir_path / extracted_file_name
            if not extracted_file_path.is_file():
                continue
            self.__cskg_version = os.path.splitext(extracted_file_name)[0].split('_', 1)[-1]
            self.__zip_file_path = extracted_file_path
            return
        raise ValueError(f"unable to find CSKG release .zip in {extracted_data_dir_path}")

    def __enter__(self):
        self.__zip_file = ZipFile(self.__zip_file_path)
        return self

    def __exit__(self, *args, **kwds):
        self.__zip_file.close()

    def open_nodes_csv(self, datasource: str):
        return TextIOWrapper(self.__zip_file.open(
            f"output_{self.__cskg_version}/{datasource}/nodes_{self.__cskg_version}.csv"), newline="\n")
