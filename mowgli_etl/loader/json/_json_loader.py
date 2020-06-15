from typing import NamedTuple, Sequence, Dict, List
import json

from mowgli_etl.model.path import Path


class _JsonLoader:
    _JSON_FILE_NAME = None

    def close(self):
        self._dump_models_to_json_file(json_file_path = self.__storage.loaded_data_dir_path / self._JSON_FILE_NAME, models = self.__models)

    @staticmethod
    def _convert_model_to_json_object(model: NamedTuple) -> Dict[str, object]:
        return {key: value for key, value in model._asdict().items() if value is not None}

    @staticmethod
    def _convert_models_to_json_array(models: Sequence[NamedTuple]) -> List[Dict[str, object]]:
        return [_JsonLoader._convert_model_to_json_object(model) for model in models]

    @staticmethod
    def _dump_models_to_json_file(*, json_file_path: Path, models: Sequence[NamedTuple]):
        with open(json_file_path, "w+") as json_file:
            json.dump(_JsonLoader._convert_models_to_json_array(models), json_file, indent=4)

    def _load_model(self, model: NamedTuple):
        self.__models.append(model)

    def open(self, storage):
        self.__models = []
        self.__storage = storage
        return self
