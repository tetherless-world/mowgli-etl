from math import floor
from typing import Generator, Tuple, Dict, List

from mowgli_etl._transformer import _Transformer
import mowgli_etl.model.concept_net_predicates
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_answer_explanation import BenchmarkAnswerExplanation
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_answer_path import BenchmarkQuestionAnswerPath
from mowgli_etl.model.benchmark_question_answer_paths import (
    BenchmarkQuestionAnswerPaths,
)
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_choice_analysis import (
    BenchmarkQuestionChoiceAnalysis,
)
from mowgli_etl.model.benchmark_dataset import BenchmarkDataset
from mowgli_etl.model.benchmark_question_choice_type import BenchmarkQuestionChoiceType
from mowgli_etl.model.benchmark_question_prompt import BenchmarkQuestionPrompt
from mowgli_etl.model.benchmark_question_prompt_type import BenchmarkQuestionPromptType
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.kg_edge import KgEdge
from mowgli_etl.model.model import Model
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl.model.kg_path import KgPath
from mowgli_etl.pipeline.portal_test_data.portal_test_data_pipeline import (
    PortalTestDataPipeline,
)
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

        paths = tuple(
            self.__transform_kg_paths(edges_by_subject=edges_by_subject, nodes=nodes)
        )
        yield from paths

        yield from self.__transform_benchmarks(paths=paths)

    def __transform_benchmarks(
        self, *, paths: Tuple[KgPath, ...]
    ) -> Generator[Model, None, None]:

        dataset_types = ("dev", "test", "train")
        for benchmark_i in range(3):
            benchmark_id = f"benchmark{benchmark_i}"
            dataset_ids = tuple(f"{benchmark_id}-{suffix}" for suffix in dataset_types)
            yield Benchmark(
                id=benchmark_id,
                name=f"Benchmark {benchmark_i}",
                datasets=tuple(
                    BenchmarkDataset(
                        id=dataset_id,
                        name=f"Benchmark {benchmark_i} {dataset_type} set",
                    )
                    for dataset_id, dataset_type in zip(dataset_ids, dataset_types)
                ),
            )
            for dataset_id, dataset_type in zip(dataset_ids, dataset_types):
                submission_id = f"{dataset_id}-submission"
                concepts = tuple(f"concept {concept_i}" for concept_i in range(5))
                for question_i in range(100):
                    question_id = f"{dataset_id}-{question_i}"
                    prompt_type = random.choice(list(BenchmarkQuestionPromptType))
                    choice_type = random.choice(list(BenchmarkQuestionChoiceType))
                    choices = tuple(
                        BenchmarkQuestionChoice(
                            id=f"{question_id}-{choice_i}",
                            identifier=chr(ord("A") + choice_i),
                            position=choice_i,
                            text=f"Choice {choice_i}",
                            type=choice_type,
                        )
                        for choice_i in range(4)
                    )
                    question = BenchmarkQuestion(
                        dataset_id=dataset_id,
                        categories=("category1", "category2"),
                        choices=choices,
                        concept=random.choice(concepts),
                        correct_choice_id=random.choice(choices).id,
                        id=question_id,
                        prompts=(
                            BenchmarkQuestionPrompt(
                                type=prompt_type,
                                text=f"Benchmark {benchmark_i} {dataset_type} set {prompt_type} {question_i}",
                            ),
                        ),
                    )
                    yield question

                    choice_analyses = []
                    for choice in question.choices:
                        question_answer_paths = []
                        for path_i in range(3):
                            path = random.choice(paths).path
                            question_answer_paths.append(
                                BenchmarkQuestionAnswerPaths(
                                    start_node_id=path[0],
                                    end_node_id=path[-1],
                                    score=random.random(),
                                    paths=(
                                        BenchmarkQuestionAnswerPath(
                                            path=path, score=random.random()
                                        ),
                                    ),
                                )
                            )
                        choice_analyses.append(
                            BenchmarkQuestionChoiceAnalysis(
                                choice_id=choice.id,
                                question_answer_paths=tuple(question_answer_paths),
                            )
                        )
                    yield BenchmarkAnswer(
                        choice_id=random.choice(question.choices).id,
                        explanation=BenchmarkAnswerExplanation(
                            choice_analyses=tuple(choice_analyses)
                        ),
                        question_id=question_id,
                        submission_id=submission_id,
                    )

                yield BenchmarkSubmission(
                    benchmark_id=benchmark_id,
                    id=submission_id,
                    dataset_id=dataset_id,
                    name=f"Benchmark {benchmark_i} test submission",
                )

    def __transform_kg_edges(
        self, nodes: Tuple[KgNode, ...]
    ) -> Generator[KgEdge, None, None]:
        concept_net_predicates = tuple(
            getattr(mowgli_etl.model.concept_net_predicates, attr)
            for attr in dir(mowgli_etl.model.concept_net_predicates)
            if not attr.startswith("_")
        )

        edge_set = MemEdgeSet()
        for subject_node in tqdm(nodes):
            out_degree = expo_int(min=10, max=200, mean=50)
            for edge_i in range(out_degree):
                while True:
                    object_node = random.choice(nodes)
                    while object_node.id == subject_node.id:
                        object_node = random.choice(nodes)
                    predicate = random.choice(concept_net_predicates)
                    edge = KgEdge.legacy(
                        datasource=PortalTestDataPipeline.ID,
                        object=object_node.id,
                        predicate=predicate,
                        subject=subject_node.id,
                        weight=floor(random.random() * 100.0) / 100.0,
                    )
                    if edge in edge_set:
                        continue
                    yield edge
                    edge_set.add(edge)
                    break

    def __transform_kg_nodes(self) -> Tuple[KgNode, ...]:
        pos = ("a", "n", "r", "v")

        return tuple(
            KgNode.legacy(
                aliases=(f"KgNode{node_i}", f"NodeAlias{node_i}"),
                datasource=PortalTestDataPipeline.ID,
                id=f"portal_test_data:{node_i}",
                label=f"Test node {node_i}",
                other={"index": node_i},
                pos=random.choice(pos),
            )
            for node_i in range(1000)
        )

    def __transform_kg_paths(
        self, *, edges_by_subject: Dict[str, List[KgEdge]], nodes: Tuple[KgNode, ...]
    ) -> Generator[KgPath, None, None]:
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
            yield KgPath(
                sources=(PortalTestDataPipeline.ID,),
                id="portal_test_data_path_" + str(path_i),
                path=tuple(path),
            )
