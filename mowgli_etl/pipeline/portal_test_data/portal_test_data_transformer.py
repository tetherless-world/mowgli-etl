from math import floor
from typing import Generator, Tuple, Dict, List

from mowgli_etl._transformer import _Transformer
import mowgli_etl.model.concept_net_predicates
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_answer_explanation import BenchmarkAnswerExplanation
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_answer_node_pair import BenchmarkQuestionAnswerNodePair
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_set import BenchmarkQuestionSet
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.model import Model
from mowgli_etl.model.node import Node
from mowgli_etl.model.path import Path
from mowgli_etl.model.scored_path import ScoredPath
from mowgli_etl.pipeline.portal_test_data.portal_test_data_pipeline import PortalTestDataPipeline
import random
from tqdm import tqdm

from mowgli_etl.storage.mem_edge_set import MemEdgeSet


# Helper functions
def expo_int(*, max: int, mean: int, min: int):
    value = floor(random.expovariate(1.0 / mean))
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


class PortalTestDataTransformer(_Transformer):
    def transform(self, **kwds):
        nodes = self.__transform_kg_nodes()
        yield from nodes

        edges_by_subject = {}
        for edge in self.__transform_kg_edges(nodes=nodes):
            edges_by_subject.setdefault(edge.subject, []).append(edge)
            yield edge

        paths = tuple(self.__transform_kg_paths(edges_by_subject=edges_by_subject, nodes=nodes))
        yield from paths

        yield from self.__transform_benchmarks(paths=paths)

    def __transform_benchmarks(self, *, paths: Tuple[Path, ...]) -> Generator[Model, None, None]:
        choices = tuple(BenchmarkQuestionChoice(
            label=chr(ord('A')+choice_i),
            text=f"Choice {choice_i}"
        ) for choice_i in range(4))

        for benchmark_i in range(3):
            benchmark_id = f"benchmark{benchmark_i}"
            yield \
                Benchmark(
                    id=benchmark_id,
                    name=f"Benchmark {benchmark_i}"
                )
            answers = []
            for question_set_id in ("dev", "test", "train"):
                question_ids = []
                concepts = tuple(f"concept {concept_i}" for concept_i in range(5))
                for question_i in range(100):
                    question_id = f"benchmark{benchmark_i}-{question_set_id}-{question_i}"
                    question_ids.append(question_id)
                    yield \
                        BenchmarkQuestion(
                            benchmark_id=benchmark_id,
                            question_set_id=question_set_id,
                            choices=choices,
                            concept=random.choice(concepts),
                            id=question_id,
                            text=f"Benchmark {benchmark_i} {question_set_id} set question {question_i}"
                        )
                yield \
                    BenchmarkQuestionSet(
                        benchmark_id=benchmark_id,
                        id=question_set_id,
                    )
                if question_set_id == "test":
                    answers = []
                    for question_id in question_ids:
                        question_answer_node_pairs = []
                        for path_i in range(3):
                            path = random.choice(paths)
                            question_answer_node_pairs.append(
                                BenchmarkQuestionAnswerNodePair(
                                    start_node_id=path[0],
                                    end_node_id=path[1],
                                    score=random.random(),
                                    paths=(
                                        ScoredPath(
                                            path=path,
                                            score=random.random()
                                        ),
                                    ),
                                )
                            )
                        answers.append(
                            BenchmarkAnswer(
                                choice_label=random.choice(choices),
                                explanation=BenchmarkAnswerExplanation(
                                    question_answer_node_pairs=tuple(question_answer_node_pairs)
                                ),
                                question_id=question_id,
                            )
                        )

                    yield \
                        BenchmarkSubmission(
                            answers=tuple(answers),
                            benchmark_id=benchmark_id,
                            question_set_id=question_set_id
                        )

    def __transform_kg_edges(self, nodes: Tuple[Node, ...]) -> Generator[Edge, None, None]:
        concept_net_predicates = tuple(getattr(mowgli_etl.model.concept_net_predicates, attr) for attr in dir(mowgli_etl.model.concept_net_predicates) if not attr.startswith("_"))

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
                            datasource=PortalTestDataPipeline.ID,
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

    def __transform_kg_nodes(self) -> Tuple[Node, ...]:
        pos = ("a", "n", "r", "v")

        return \
            tuple(
                Node(
                    datasource=PortalTestDataPipeline.ID,
                    aliases=(f"Node {node_i}", f"Node alias {node_i}"),
                    id=f"portal_test_data:{node_i}",
                    label=f"Test node {node_i}",
                    other={"index": node_i},
                    pos=random.choice(pos),
                )
                for node_i in range(1000)
            )

    def __transform_kg_paths(self, *, edges_by_subject: Dict[str, List[Edge]], nodes: Tuple[Node, ...]) -> Generator[Path, None, None]:
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
                        # Prevent loops
                        break
                # print(current_node_id, choose_edge.predicate, choose_edge.object)
                path.append(choose_edge.predicate)
                path.append(choose_edge.object)
                path_node_ids.add(choose_edge.object)
                current_node_id = choose_edge.object
            yield Path(
                datasource=PortalTestDataPipeline.ID,
                id="portal_test_data_path_" + str(path_i),
                path=tuple(path)
            )
