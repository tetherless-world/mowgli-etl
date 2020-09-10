from csv import DictWriter
from pathlib import Path

from mowgli_etl.loader._kg_edge_loader import _KgEdgeLoader
from mowgli_etl.loader._kg_node_loader import _KgNodeLoader
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.kg_node import KgNode
try:
    from mowgli_etl.storage.persistent_kg_node_set import PersistentKgNodeSet as NodeSet
except ImportError:
    from mowgli_etl.storage.mem_kg_node_set import MemKgNodeSet as NodeSet


class KgtkEdgesTsvLoader(_KgEdgeLoader, _KgNodeLoader):
    __HEADER = """node1	relation	node2	node1;label	node2;label	relation;label	relation;dimension	weight	source	origin	sentence	question	id"""

    def __init__(self, bzip: bool = False):
        _KgEdgeLoader.__init__(self)
        _KgNodeLoader.__init__(self)
        self.__bzip = bzip

    def close(self):
        self.__edges_file.close()
        self.__node_set.close()
        if self.__bzip:
            self._bzip_file(Path(self.__edges_file.name))

    def open(self, storage):
        self.__edges_file = open(storage.loaded_data_dir_path / "edges.tsv", "w+")
        writer_opts = {'delimiter': '\t', 'lineterminator': '\n'}
        self.__edges_writer = DictWriter(self.__edges_file, self.__HEADER.split(), **writer_opts)
        self.__edges_writer.writeheader()
        self.__node_set = NodeSet.temporary()
        return self

    def load_kg_edge(self, edge: KgEdge):
        object_node = self.__node_set.get(edge.object)
        if object_node is None:
            raise ValueError(f"missing edge object node {edge.object}")
        subject_node = self.__node_set.get(edge.subject)
        if subject_node is None:
            raise ValueError(f"missing edge subject node {edge.subject}")

        self.__edges_writer.writerow({
            "id": edge.id,
            "node1": edge.subject,
            "node1;label": "|".join(subject_node.labels),
            "node2": edge.object,
            "node2;label": "|".join(object_node.labels),
            "relation": edge.predicate,
            "source": "|".join(edge.source_ids),
            "weight": edge.weight if edge.weight is not None else "",
        })

    def load_kg_node(self, node: KgNode):
        if node.id not in self.__node_set:
            self.__node_set.add(node)
