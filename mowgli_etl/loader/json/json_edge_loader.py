from mowgli_etl.loader._kg_edge_loader import _KgEdgeLoader

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonEdgeLoader(_KgEdgeLoader, _JsonLoader):
    _JSON_FILE_NAME = "edges.json"
    close = _JsonLoader.close
    load_kg_edge = _JsonLoader._load_model
    open = _JsonLoader.open
