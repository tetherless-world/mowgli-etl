import os.path
from pathlib import Path


class PipelineStorage:
    def __init__(self, *, pipeline_id: str, root_data_dir_path: Path):
        self.__root_data_dir_path = root_data_dir_path
        pipeline_data_dir_path = root_data_dir_path / Path(pipeline_id)
        self.__extracted_data_dir_path = self.__makedirs(pipeline_data_dir_path / "extracted")
        self.__loaded_data_dir_path = self.__makedirs(pipeline_data_dir_path / "loaded")
        self.__transformed_data_dir_path = self.__makedirs(pipeline_data_dir_path / "transformed")

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
    def root_data_dir_path(self) -> Path:
        return self.__root_data_dir_path

    @property
    def transformed_data_dir_path(self) -> Path:
        return self.__transformed_data_dir_path
