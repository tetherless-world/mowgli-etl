from mowgli_etl.loader._node_loader import _NodeLoader

from mowgli_etl.loader._path_loader import _PathLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonPathLoader(_PathLoader, _JsonLoader):
    _JSON_FILE_NAME = "paths.json"
    close = _JsonLoader.close
    load_path = _JsonLoader._load_model
    open = _JsonLoader.open
