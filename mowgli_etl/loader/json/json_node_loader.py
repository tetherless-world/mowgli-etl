from mowgli_etl._node_loader import _NodeLoader
import json


class JsonNodeLoader(_NodeLoader):
    def close(self):
        with open(self.__storage.loaded_data_dir_path / "nodes.json", "w+") as json_file:
            json.dump(self.__nodes, json_file)

    def load_node(self, node):
        self.__nodes.append(node)

    def open(self, storage):
        self.__nodes = []
        self.__storage = storage
        return self
