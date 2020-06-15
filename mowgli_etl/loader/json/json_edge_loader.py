from mowgli_etl.loader._edge_loader import _EdgeLoader
import json

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonEdgeLoader(_EdgeLoader, _JsonLoader):
    def __init__(self):
        _EdgeLoader.__init__(self)
        _JsonLoader.__init__(self, json_file_name="edges.json")

    def close(self, *args, **kwds):
        return _JsonLoader.close(self, *args, **kwds)

    def load_edge(self, edge):
        self._load_model(edge)

    def open(self, *args, **kwds):
        return _JsonLoader.open(self, *args, **kwds)
