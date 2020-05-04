from typing import Generator

from mowgli.lib.cskg import mowgli_predicates
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.mapper.concept_net.concept_net_index import ConceptNetIndex


class ConceptNetMapper:
    def __init__(self, concept_net_index: ConceptNetIndex):
        self.__concept_net_index = concept_net_index

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
