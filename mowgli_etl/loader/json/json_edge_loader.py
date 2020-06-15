from mowgli_etl.loader._edge_loader import _EdgeLoader

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonEdgeLoader(_EdgeLoader, _JsonLoader):
    _JSON_FILE_NAME = "edges.json"
    close = _JsonLoader.close
    load_edge = _JsonLoader._load_model
    open = _JsonLoader.open
