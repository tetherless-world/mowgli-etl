import collections
from typing import NamedTuple
import json

# Helper functions
import stringcase


def isinstance_namedtuple(x):
    if not isinstance(x, tuple):
        return False
    # if not isinstance(getattr(x, '__dict__', None), collections.Mapping):
    #     return False
    if getattr(x, '_fields', None) is None:
        return False
    return True


class _JsonLoader:
    _JSON_FILE_NAME = None

    def close(self):
        with open(self.__storage.loaded_data_dir_path / self._JSON_FILE_NAME, "w+") as json_file:
            json.dump(_JsonLoader._convert_to_json(self.__models), json_file, indent=4)

    @staticmethod
    def _convert_to_json(obj):
        if isinstance_namedtuple(obj):
            # Model/named tuple
            return {stringcase.camelcase(key): _JsonLoader._convert_to_json(value) for key, value in obj._asdict().items() if value is not None}
        elif isinstance(obj, (list, tuple)):
            return [_JsonLoader._convert_to_json(element) for element in obj]
        else:
            return obj

    def _load_model(self, model: NamedTuple):
        self.__models.append(model)

    def open(self, storage):
        self.__models = []
        self.__storage = storage
        return self
