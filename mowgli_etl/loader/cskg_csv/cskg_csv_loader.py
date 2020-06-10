from mowgli_etl._edge_loader import _EdgeLoader
from mowgli_etl._node_loader import _NodeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_edge_loader import CskgCsvEdgeLoader
from mowgli_etl.loader.cskg_csv.cskg_csv_node_loader import CskgCsvNodeLoader
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node


class CskgCsvLoader(_EdgeLoader, _NodeLoader):
    def __init__(self, *, bzip: bool = False):
        self.__edge_loader = CskgCsvEdgeLoader(bzip=bzip)
        self.__node_loader = CskgCsvNodeLoader(bzip=bzip)

    def open(self, storage):
        self.__edge_loader.open(storage)
        self.__node_loader.open(storage)
        return self

    def close(self):
        self.__edge_loader.close()
        self.__node_loader.close()

    def load_edge(self, edge: Edge):
        self.__edge_loader.load_edge(edge)

    def load_node(self, node: Node):
        self.__node_loader.load_node(node)
