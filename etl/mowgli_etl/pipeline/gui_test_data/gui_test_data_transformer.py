from mowgli_etl._transformer import _Transformer
import mowgli_etl.cskg.concept_net_predicates
from mowgli_etl.cskg.edge import Edge
from mowgli_etl.cskg.node import Node
from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
import random

from mowgli_etl.storage.mem_edge_set import MemEdgeSet


class GuiTestDataTransformer(_Transformer):
    def transform(self, **kwds):
        concept_net_predicates = tuple(getattr(mowgli_etl.cskg.concept_net_predicates, attr) for attr in dir(mowgli_etl.cskg.concept_net_predicates) if not attr.startswith("_"))

        pos = ("a", "n", "r", "v")

        nodes = \
            tuple(
                Node(
                    datasource=GuiTestDataPipeline.ID,
                    aliases=(f"Node {node_i}", f"Node alias {node_i}"),
                    id=f"gui_test_data:{node_i}",
                    label=f"Test node {node_i}",
                    other={"index": node_i},
                    pos=random.choice(pos),
                )
                for node_i in range(1000)
            )
        yield from nodes

        for subject_node in nodes:
            edge_set = MemEdgeSet()
            for edge_i in range(100):
                while True:
                    object_node = random.choice(nodes)
                    while object_node.id == subject_node.id:
                        object_node = random.choice(nodes)
                    predicate = random.choice(concept_net_predicates)
                    edge = \
                        Edge(
                            datasource=GuiTestDataPipeline.ID,
                            object=object_node.id,
                            other={"index": edge_i},
                            predicate=predicate,
                            subject=subject_node.id,
                            weight=random.random()
                        )
                    if edge in edge_set:
                        continue
                    yield edge
                    edge_set.add(edge)
                    break
