from mowgli_etl.loader._kg_node_loader import _KgNodeLoader

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonNodeLoader(_KgNodeLoader, _JsonLoader):
    _JSON_FILE_NAME = "nodes.json"
    close = _JsonLoader.close
    load_kg_node = _JsonLoader._load_model
    open = _JsonLoader.open
