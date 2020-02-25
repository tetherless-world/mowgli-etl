import os.path
from pathlib import Path


class PipelineStorage:
    def __init__(self, data_dir_path: Path, pipeline_id: str):
        self.__extracted_data_dir_path = self.__makedirs(data_dir_path / pipeline_id / "extracted")
        self.__loaded_data_dir_path = self.__makedirs(data_dir_path / pipeline_id / "loaded")
        self.__transformed_data_dir_path = self.__makedirs(data_dir_path / pipeline_id / "transformed")

    def __makedirs(self, dir_path: Path) -> Path:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return dir_path

    @property
    def extracted_data_dir_path(self) -> Path:
        return self.__extracted_data_dir_path

    @property
    def loaded_data_dir_path(self) -> Path:
        return self.__loaded_data_dir_path

    @property
    def transformed_data_dir_path(self) -> Path:
        return self.__transformed_data_dir_path
