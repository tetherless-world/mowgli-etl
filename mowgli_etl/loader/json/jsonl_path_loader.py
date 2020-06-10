from mowgli_etl._path_loader import _PathLoader
import json


class JsonlPathLoader(_PathLoader):
    def close(self):
        self.__paths_jsonl_file.close()

    def load_path(self, path):
        json.dump({key: value for key, value in path._asdict().items() if value is not None}, self.__paths_jsonl_file)
        self.__paths_jsonl_file.write("\n")

    def open(self, storage):
        # Ignore PipelineStorage passed in, write to the GUI test data directory
        self.__paths_jsonl_file = open(storage.loaded_data_dir_path / "paths.jsonl", "w+")
        return self
