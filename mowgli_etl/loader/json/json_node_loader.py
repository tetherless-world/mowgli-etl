from mowgli_etl.loader._node_loader import _NodeLoader
import json

from mowgli_etl.loader.json._json_loader import _JsonLoader


class JsonNodeLoader(_NodeLoader, _JsonLoader):
    def __init__(self):
        _NodeLoader.__init__(self)
        _JsonLoader.__init__(self, json_file_name="nodes.json")

    def close(self, *args, **kwds):
        return _JsonLoader.close(self, *args, **kwds)

    def load_node(self, node):
        self._load_model(node)

    def open(self, *args, **kwds):
        return _JsonLoader.open(self, *args, **kwds)
