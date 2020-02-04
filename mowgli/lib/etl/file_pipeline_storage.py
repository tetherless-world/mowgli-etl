import os.path
from io import IOBase

from pathvalidate import sanitize_filename

from mowgli.lib.etl._pipeline_storage import _PipelineStorage


class FilePipelineStorage(_PipelineStorage):
    def __init__(self, root_dir_path: str):
        self.__root_dir_path = root_dir_path

    @classmethod
    def create(cls, root_dir_path: str):
        if not os.path.isdir(root_dir_path):
            os.makedirs(root_dir_path)
        return cls(root_dir_path)

    def get(self, key):
        file_path = self.__key_to_file_path(key)
        return open(file_path, "rb")

    def head(self, key):
        file_path = self.__key_to_file_path(key)
        return os.path.isfile(file_path)

    def __key_to_file_path(self, key: str):
        return os.path.join(self.__root_dir_path, sanitize_filename(key))

    def put(self, key, value):
        file_path = self.__key_to_file_path(key)
        if isinstance(value, IOBase):
            value = value.read()
        elif isinstance(value, str):
            value = value.encode("utf-8")
        result = os.path.isfile(file_path)
        with open(file_path, "w+b") as f:
            f.write(value)
        return result
