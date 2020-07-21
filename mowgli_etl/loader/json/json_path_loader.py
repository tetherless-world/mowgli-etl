from mowgli_etl.loader._kg_node_loader import _KgNodeLoader

from mowgli_etl.loader._kg_path_loader import _KgPathLoader
from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonPathLoader(_KgPathLoader, _JsonLoader):
    _JSON_FILE_NAME = "paths.json"
    close = _JsonLoader.close
    load_kg_path = _JsonLoader._load_model
    open = _JsonLoader.open
