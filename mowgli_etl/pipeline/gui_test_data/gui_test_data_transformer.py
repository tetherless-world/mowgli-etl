from math import floor

from mowgli_etl._transformer import _Transformer
import mowgli_etl.model.concept_net_predicates
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.pipeline.gui_test_data.gui_test_data_pipeline import GuiTestDataPipeline
import random
from tqdm import tqdm

from mowgli_etl.storage.mem_edge_set import MemEdgeSet


class GuiTestDataTransformer(_Transformer):
    def transform(self, **kwds):
        concept_net_predicates = tuple(getattr(mowgli_etl.model.concept_net_predicates, attr) for attr in dir(mowgli_etl.model.concept_net_predicates) if not attr.startswith("_"))

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

        out_degree_mean = 50
        out_degree_min = 10
        out_degree_max = 200
        out_degree_lambda = 1.0 / out_degree_mean
        for subject_node in tqdm(nodes):
            edge_set = MemEdgeSet()
            out_degree = floor(random.expovariate(out_degree_lambda))
            if out_degree < out_degree_min:
                out_degree = out_degree_min
            elif out_degree > out_degree_max:
                out_degree = out_degree_max
            for edge_i in range(out_degree):
                while True:
                    object_node = random.choice(nodes)
                    while object_node.id == subject_node.id:
                        object_node = random.choice(nodes)
                    predicate = random.choice(concept_net_predicates)
                    edge = \
                        Edge(
                            datasource=GuiTestDataPipeline.ID,
                            object=object_node.id,
                            predicate=predicate,
                            subject=subject_node.id,
                            weight=floor(random.random() * 100.0) / 100.0
                        )
                    if edge in edge_set:
                        continue
                    yield edge
                    edge_set.add(edge)
                    break
