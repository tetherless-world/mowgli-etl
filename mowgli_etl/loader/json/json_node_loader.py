from mowgli_etl.loader._node_loader import _NodeLoader

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonNodeLoader(_NodeLoader, _JsonLoader):
    _JSON_FILE_NAME = "nodes.json"
    close = _JsonLoader.close
    load_node = _JsonLoader._load_model
    open = _JsonLoader.open
