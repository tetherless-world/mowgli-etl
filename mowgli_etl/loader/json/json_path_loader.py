import json

from mowgli_etl._path_loader import _PathLoader


class JsonPathLoader(_PathLoader):
    def close(self):
        with open(self.__storage.loaded_data_dir_path / "paths.json", "w+") as json_file:
            json.dump(self.__paths, json_file)

    def load_path(self, path):
        self.__paths.append({key: value for key, value in path._asdict().items() if value is not None})

    def open(self, storage):
        self.__paths = []
        self.__storage = storage
        return self
