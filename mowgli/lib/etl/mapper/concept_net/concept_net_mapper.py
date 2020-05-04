from typing import Generator

from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.mapper.concept_net.concept_net_label_index import ConceptNetLabelIndex


class ConceptNetMapper:
    def __init__(self):
        self.__concept_net_label_index = None

    def map(self, node: Node) -> Generator[Edge, None, None]:
        """
        Given a node from another data source, generate a sequence of edges mapping that node to ConceptNet concepts.
        """
        if self.__concept_net_label_index is None:
            self.__concept_net_label_index = ConceptNetLabelIndex.open()
