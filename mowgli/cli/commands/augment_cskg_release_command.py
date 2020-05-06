import os.path
import shutil
from pathlib import Path

from configargparse import ArgParser

from mowgli import paths
from mowgli.cli.commands._command import _Command


class AugmentCskgReleaseCommand(_Command):
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
                os.path.splitext(cskg_release_zip_file_path.name)[0] + "-rpi.zip")
        augmented_cskg_release_zip_file_path.unlink(missing_ok=True)
        self._logger.info("copying CSKG release .zip %s to %s", cskg_release_zip_file_path,
                          augmented_cskg_release_zip_file_path)
        shutil.copy(cskg_release_zip_file_path, augmented_cskg_release_zip_file_path)

        with open(augmented_cskg_release_zip_file_path, mode="a") as augmented_cskg_release_zip_file:
            for data_source_name in os.listdir(data_dir_path):
                data_source_path = data_dir_path / data_source_name
                if not data_source_path.is_dir():
                    continue
                loaded_dir_path = data_source_path / "loaded"
                if not loaded_dir_path.is_dir():
                    self._logger.debug("%s has no loaded directory, skipping", data_source_name)
                    continue

                csv_file_stems = ("edges", "nodes")
                csv_file_paths = tuple(loaded_dir_path / (csv_file_stem + ".csv") for csv_file_stem in csv_file_stems)
                if not all(csv_file_path.is_file() for csv_file_path in csv_file_paths):
                    self._logger.debug("%s is missing a nodes or edges .csv, skipping", data_source_name)
                    continue
                for csv_file_stem, csv_file_path in zip(csv_file_stem, csv_file_paths):
                    csv_file_path_within_zip = f"output_{cskg_version}/{data_source_name}/{csv_file_stem}_{cskg_version}.csv"
                    augmented_cskg_release_zip_file.write(csv_file_path_within_zip)
                    self._logger.info("copying %s to %s within the augmented .zip", csv_file_path,
                                      csv_file_path_within_zip)
                    with open(csv_file_path, mode="rb") as csv_file:
                        with augmented_cskg_release_zip_file.open(csv_file_path_within_zip,
                                                                  mode="w") as csv_file_within_zip:
                            while True:
                                buffer = csv_file.read()
                                if not buffer:
                                    break
                                csv_file_within_zip.write(buffer)
                    self._logger.info("copied %s to %s within the augmented .zip", csv_file_path,
                                      csv_file_path_within_zip)


def __find_cskg_release_zip_file(self, *, data_dir_path: Path) -> Path:
    extracted_data_dir_path = data_dir_path / "cskg_release" / "extracted"
    for extracted_file_name in os.listdir(extracted_data_dir_path):
        if os.path.splitext(extracted_file_name)[1] != ".zip":
            continue
        extracted_file_path = extracted_data_dir_path / extracted_file_name
        if not extracted_file_path.is_file():
            continue
        cskg_release_zip_file_path = extracted_file_path
        break
    if cskg_release_zip_file_path is None:
        raise ValueError(f"unable to find CSKG release .zip in {extracted_data_dir_path}")
    return cskg_release_zip_file_path
