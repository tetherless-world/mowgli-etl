import os.path
import shutil
from io import BytesIO
from pathlib import Path
from typing import Tuple
from zipfile import ZipFile

from configargparse import ArgParser

from mowgli import paths
from mowgli.cli.commands._command import _Command


class AugmentCskgReleaseCommand(_Command):
    __CSV_FILE_STEMS = ("edges", "nodes")

    def add_arguments(self, arg_parser: ArgParser, add_parent_args):
        arg_parser.add_argument("--cskg-release-zip-file-path", help="path to a CSKG release .zip file")
        arg_parser.add_argument(
            "--data-dir-path",
            default=str(paths.DATA_DIR),
            help="path to a directory to store extracted and transformed data",
        )

    def __call__(self, args):
        data_dir_path = Path(args.data_dir_path)

        cskg_release_zip_file_path = args.cskg_release_zip_file_path
        if cskg_release_zip_file_path is None:
            cskg_release_zip_file_path = self.__find_cskg_release_zip_file(data_dir_path=data_dir_path)
        cskg_version = os.path.splitext(cskg_release_zip_file_path.name)[0].split('_', 1)[-1]

        # Copy the .zip file and then modify it in place
        augmented_cskg_release_zip_file_path = cskg_release_zip_file_path.parent / (
                os.path.splitext(cskg_release_zip_file_path.name)[0] + "_rpi.zip")
        if augmented_cskg_release_zip_file_path.is_file():
            self._logger.info("deleting existed augmented .zip %s", augmented_cskg_release_zip_file_path)
            augmented_cskg_release_zip_file_path.unlink()
        self._logger.info("copying CSKG release .zip %s to %s", cskg_release_zip_file_path,
                          augmented_cskg_release_zip_file_path)
        shutil.copy(cskg_release_zip_file_path, augmented_cskg_release_zip_file_path)

        with ZipFile(augmented_cskg_release_zip_file_path, mode="a") as augmented_cskg_release_zip_file:
            for data_source_name in os.listdir(data_dir_path):
                csv_file_paths = self.__find_rpi_csv_files(data_dir_path=data_dir_path,
                                                           data_source_name=data_source_name)
                if not csv_file_paths:
                    continue

                self.__copy_rpi_csv_files(augmented_cskg_release_zip_file=augmented_cskg_release_zip_file,
                                          cskg_version=cskg_version, csv_file_paths=csv_file_paths,
                                          data_source_name=data_source_name)

                if data_source_name == "rpi_combined":
                    self.__append_rpi_combined_csv_files(
                        augmented_cskg_release_zip_file=augmented_cskg_release_zip_file,
                        cskg_release_zip_file_path=cskg_release_zip_file_path,
                        cskg_version=cskg_version,
                        csv_file_paths=csv_file_paths
                    )

    def __append_rpi_combined_csv_files(self, *, augmented_cskg_release_zip_file: ZipFile,
                                        cskg_release_zip_file_path: Path, cskg_version: str,
                                        csv_file_paths: Tuple[Path, Path]):
        def copy_streams(src: BytesIO, dst: BytesIO):
            while True:
                buffer = src.read(1024 * 1024)  # read() reads too much at a time
                if not buffer:
                    return
                dst.write(buffer)

        for csv_file_stem, csv_file_path in zip(self.__CSV_FILE_STEMS, csv_file_paths):
            cskg_release_csv_file_path = f"output_{cskg_version}/cskg-raw/{csv_file_stem}_{cskg_version}.csv"
            combined_csv_file_path = f"output_{cskg_version}/cskg-raw-rpi/{csv_file_stem}_{cskg_version}.csv"
            self._logger.info("concatenating %s with %s to create %s within .zip file", csv_file_path,
                              cskg_release_csv_file_path, combined_csv_file_path)
            # Can't append to an existing file in the .zip, so have to create a new one
            with augmented_cskg_release_zip_file.open(combined_csv_file_path, "w") as combined_csv_file:
                # Read from the original .zip file because we can't have read while we also have a write handle open on a single .zip file
                with ZipFile(cskg_release_zip_file_path) as cskg_release_zip_file:
                    with cskg_release_zip_file.open(cskg_release_csv_file_path) as cskg_release_csv_file:
                        copy_streams(cskg_release_csv_file, combined_csv_file)
                with open(csv_file_path, "rb") as rpi_csv_file:
                    # Discard the header line
                    while rpi_csv_file.read(1) != b"\n":
                        continue
                    copy_streams(rpi_csv_file, combined_csv_file)
            self._logger.info("concatenated %s with %s to create %s within .zip file", csv_file_path,
                              cskg_release_csv_file_path, combined_csv_file_path)

    def __copy_rpi_csv_files(self, *, augmented_cskg_release_zip_file: ZipFile, cskg_version: str,
                             csv_file_paths: Tuple[Path, str], data_source_name: str):
        for csv_file_stem, csv_file_path in zip(self.__CSV_FILE_STEMS, csv_file_paths):
            csv_file_path_within_zip = f"output_{cskg_version}/{data_source_name}/{csv_file_stem}_{cskg_version}.csv"
            self._logger.info("copying %s to %s within the augmented .zip", csv_file_path,
                              csv_file_path_within_zip)
            augmented_cskg_release_zip_file.write(csv_file_path, arcname=csv_file_path_within_zip)
            self._logger.info("copied %s to %s within the augmented .zip", csv_file_path,
                              csv_file_path_within_zip)

    def __find_cskg_release_zip_file(self, *, data_dir_path: Path) -> Path:
        extracted_data_dir_path = data_dir_path / "cskg_release" / "extracted"
        for extracted_file_name in os.listdir(extracted_data_dir_path):
            extracted_file_stem, extracted_file_ext = os.path.splitext(extracted_file_name)
            if extracted_file_ext != ".zip":
                continue
            elif extracted_file_stem.endswith("_rpi"):
                continue
            extracted_file_path = extracted_data_dir_path / extracted_file_name
            if not extracted_file_path.is_file():
                continue
            cskg_release_zip_file_path = extracted_file_path
            break
        if cskg_release_zip_file_path is None:
            raise ValueError(f"unable to find CSKG release .zip in {extracted_data_dir_path}")
        return cskg_release_zip_file_path

    def __find_rpi_csv_files(self, *, data_dir_path: Path, data_source_name: str):
        data_source_path = data_dir_path / data_source_name
        if not data_source_path.is_dir():
            return None
        loaded_dir_path = data_source_path / "loaded"
        if not loaded_dir_path.is_dir():
            self._logger.debug("%s has no loaded directory, skipping", data_source_name)
            return None

        csv_file_paths = tuple(
            loaded_dir_path / (csv_file_stem + ".csv") for csv_file_stem in self.__CSV_FILE_STEMS)
        if not all(csv_file_path.is_file() for csv_file_path in csv_file_paths):
            self._logger.debug("%s is missing a nodes or edges .csv, skipping", data_source_name)
            return None
        return csv_file_paths
