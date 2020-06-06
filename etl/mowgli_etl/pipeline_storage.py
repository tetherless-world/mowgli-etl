import os.path
from pathlib import Path
from typing import Optional


class PipelineStorage:
    def __init__(self, *, pipeline_id: str, root_data_dir_path: Path, extracted_data_dir_path: Optional[Path] = None, loaded_data_dir_path: Optional[Path] = None):
        self.__root_data_dir_path = root_data_dir_path
        pipeline_data_dir_path = root_data_dir_path / Path(pipeline_id)

        if extracted_data_dir_path is None:
            extracted_data_dir_path = pipeline_data_dir_path / "extracted"
        self.__extracted_data_dir_path = extracted_data_dir_path
        self.__extracted_data_dir_path_exists = False

        if loaded_data_dir_path is None:
            loaded_data_dir_path = pipeline_data_dir_path / "loaded"
        self.__loaded_data_dir_path = loaded_data_dir_path
        self.__loaded_data_dir_path_exists = False
        # self.__transformed_data_dir_path = self.__makedirs(pipeline_data_dir_path / "transformed")

    def __makedirs(self, dir_path: Path) -> Path:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return dir_path

    @property
    def extracted_data_dir_path(self) -> Path:
        if not self.__extracted_data_dir_path_exists:
            self.__makedirs(self.__extracted_data_dir_path)
            self.__extracted_data_dir_path_exists = True
        return self.__extracted_data_dir_path

    @property
    def loaded_data_dir_path(self) -> Path:
        if not self.__loaded_data_dir_path_exists:
            self.__makedirs(self.__loaded_data_dir_path)
            self.__loaded_data_dir_path_exists = True
        return self.__loaded_data_dir_path

    @property
    def root_data_dir_path(self) -> Path:
        return self.__root_data_dir_path

    # @property
    # def transformed_data_dir_path(self) -> Path:
    #     return self.__transformed_data_dir_path
