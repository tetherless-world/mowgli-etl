from mowgli_etl._edge_loader import _EdgeLoader
import json


class JsonEdgeLoader(_EdgeLoader):
    def close(self):
        with open(self.__storage.loaded_data_dir_path / "edges.json", "w+") as json_file:
            json.dump(self.__edges, json_file)

    def load_edge(self, edge):
        self.__edges.append(edge)

    def open(self, storage):
        self.__edges = []
        self.__storage = storage
        return self
