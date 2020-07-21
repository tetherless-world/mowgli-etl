from csv import DictWriter

from mowgli_etl.loader._edge_loader import _EdgeLoader
from mowgli_etl.loader._node_loader import _NodeLoader
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
try:
    from mowgli_etl.storage.persistent_node_set import PersistentNodeSet as NodeSet
except ImportError:
    from mowgli_etl.storage.mem_node_set import MemNodeSet as NodeSet


class KgtkEdgesTsvLoader(_EdgeLoader, _NodeLoader):
    __HEADER = """node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question	id"""

    def close(self):
        self.__edges_file.close()
        self.__node_set.close()

    def open(self, storage):
        self.__edges_file = open(storage.loaded_data_dir_path / "edges.tsv", "w+")
        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__edges_writer = DictWriter(self.__edges_file, self.__HEADER.split(), **writer_opts)
        self.__edges_writer.writeheader()
        self.__node_set = NodeSet.temporary()
        return self

    def load_edge(self, edge: Edge):
        object_node = self.__node_set.get(edge.object)
        if object_node is None:
            raise ValueError(f"missing edge object node {edge.object}")
        subject_node = self.__node_set.get(edge.subject)
        if subject_node is None:
            raise ValueError(f"missing edge subject node {edge.subject}")

        self.__edges_writer.writerow({
            "id": f"{edge.subject}-{edge.predicate}-{edge.object}",
            "node1": edge.subject,
            "node1;label": subject_node.label,
            "node2": edge.object,
            "node2;label": object_node.label,
            "relation": edge.predicate,
            "source": edge.datasource,
            "weight": edge.weight,
        })

    def load_node(self, node: Node):
        if node.id not in self.__node_set:
            self.__node_set.add(node)
