from mowgli_etl.loader._node_loader import _NodeLoader
import json

from mowgli_etl.loader._path_loader import _PathLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonPathLoader(_PathLoader, _JsonLoader):
    def __init__(self):
        _NodeLoader.__init__(self)
        _JsonLoader.__init__(self, json_file_name="paths.json")

    def close(self, *args, **kwds):
        return _JsonLoader.close(self, *args, **kwds)

    def load_path(self, path):
        self._load_model(path)

    def open(self, *args, **kwds):
        return _JsonLoader.open(self, *args, **kwds)
