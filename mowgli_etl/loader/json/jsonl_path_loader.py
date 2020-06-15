from mowgli_etl.loader._path_loader import _PathLoader
import json

from mowgli_etl.loader.json._jsonl_loader import _JsonlLoader


class JsonlPathLoader(_PathLoader, _JsonlLoader):
    def __init__(self):
        _PathLoader.__init__(self)
        _JsonlLoader.__init__(self, jsonl_file_name="paths.jsonl")

    def close(self, *args, **kwds):
        return _JsonlLoader.close(self, *args, **kwds)

    def load_path(self, path):
        self._load_model(path)

    def open(self, *args, **kwds):
        return _JsonlLoader.open(self, *args, **kwds)
