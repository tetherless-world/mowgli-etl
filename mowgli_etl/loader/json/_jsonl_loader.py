import json
from typing import NamedTuple

from mowgli_etl.loader.json._json_loader import _JsonLoader


class _JsonlLoader:
    _JSONL_FILE_NAME = None

    def close(self):
        self.__jsonl_file.close()

    def _load_model(self, model: NamedTuple):
        json.dump(_JsonLoader._convert_model_to_json_object(model), self.__jsonl_file)
        self.__jsonl_file.write("\n")

    def open(self, storage):
        self.__jsonl_file = open(storage.loaded_data_dir_path / self._JSONL_FILE_NAME, "w+")
        return self
