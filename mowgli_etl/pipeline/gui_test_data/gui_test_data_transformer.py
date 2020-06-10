from math import floor

from mowgli_etl._transformer import _Transformer
import mowgli_etl.model.concept_net_predicates
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.model.path import Path
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

        def expo_int(*, max: int, mean: int, min: int):
            value = floor(random.expovariate(1.0 / mean))
            if value < min:
                return min
            elif value > max:
                return max
            else:
                return value

        edges_by_subject = {}
        edge_set = MemEdgeSet()
        for subject_node in tqdm(nodes):
            out_degree = expo_int(min=10, max=200, mean=50)
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
                    edges_by_subject.setdefault(subject_node.id, []).append(edge)
                    break

        for path_i in range(10):
            current_node_id = start_node_id = random.choice(nodes).id
            path_length = expo_int(max=20, min=4, mean=10)
            path_node_ids = set(start_node_id)
            path = [start_node_id]
            # print("Start:", current_node_id)
            for link_i in range(path_length):
                current_node_edges = edges_by_subject[current_node_id]
                while True:
                    choose_edge = random.choice(current_node_edges)
                    if choose_edge.object not in path_node_ids:
                        break
                # print(current_node_id, choose_edge.predicate, choose_edge.object)
                path.append(choose_edge.predicate)
                path.append(choose_edge.object)
                path_node_ids.add(choose_edge.object)
                current_node_id = choose_edge.object
            yield Path(
                datasource=GuiTestDataPipeline.ID,
                id="gui_test_data_path_" + str(path_i),
                path=tuple(path)
            )
