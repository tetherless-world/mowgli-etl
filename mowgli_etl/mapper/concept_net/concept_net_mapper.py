from typing import Generator

from mowgli_etl._closeable import _Closeable
from mowgli_etl.model import mowgli_predicates
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.mapper.concept_net.concept_net_index import ConceptNetIndex


class ConceptNetMapper(_Closeable):
    def __init__(self, concept_net_index: ConceptNetIndex):
        self.__concept_net_index = concept_net_index

    def close(self):
        self.__concept_net_index.close()

    def map(self, node: Node) -> Generator[Edge, None, None]:
        """
        Given a node from another data source, generate a sequence of edges mapping that node to ConceptNet concepts.
        """
        concept_net_id = self.__concept_net_index.get(label=node.label, pos=node.pos)
        if concept_net_id is None:
            return
        yield \
            Edge(
                datasource=node.datasource,
                object=concept_net_id,
                predicate=mowgli_predicates.SAME_AS,
                subject=node.id,
            )