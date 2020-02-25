from abc import ABC, abstractmethod
from io import IOBase
from pathlib import Path
from typing import Union


class PipelineStorage:
    def __init__(self, data_dir_path: Path, pipeline_id: str):
        self.__extracted_data_dir_path = data_dir_path / pipeline_id / "extracted"
        self.__loaded_data_dir_path = data_dir_path / pipeline_id / "loaded"
        self.__transformed_data_dir_path = data_dir_path / pipeline_id / "transformed"

    @property
    def extracted_data_dir_path(self) -> Path:
        return self.__extracted_data_dir_path

    @property
    def loaded_data_dir_path(self) -> Path:
        return self.__loaded_data_dir_path

    @property
    def transformed_data_dir_path(self) -> Path:
        return self.__transformed_data_dir_path
