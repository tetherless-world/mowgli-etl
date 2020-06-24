import json
from pathlib import Path
from typing import NamedTuple

from mowgli_etl._loader import _Loader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class _JsonlLoader(_Loader):
    _JSONL_FILE_NAME = None

    def __init__(self, bzip: bool = False):
        _Loader.__init__(self)
        self.__bzip = bzip

    def close(self):
        self.__jsonl_file.close()
        if self.__bzip:
            self._bzip_file(Path(self.__jsonl_file.name))

    def _load_model(self, model: NamedTuple, bzip: bool = False):
        json.dump(_JsonLoader._convert_to_json(model), self.__jsonl_file)
        self.__jsonl_file.write("\n")

    def open(self, storage):
        self.__jsonl_file = open(storage.loaded_data_dir_path / self._JSONL_FILE_NAME, "w+")
        return self
