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

from mowgli_etl.storage.mem_id_set import MemIdSet
from mowgli_etl.storage.mem_kg_edge_set import MemKgEdgeSet


# Helper functions
# def expo_int(*, max: int, mean: int, min: int):
#     assert min >= 1
#     assert min < max
#     assert mean > min and mean < max
#     value = floor(random.expovariate(1.0 / mean))
#     if value < min:
#         return min
#     elif value > max:
#         return max
#     else:
#         return value


class PortalTestDataTransformer(_Transformer):
    __SECONDARY_SOURCES = tuple(f"portal_test_data_secondary_{i}" for i in range(3))

    def transform(self, **kwds):
        nodes = self.__generate_kg_nodes()
        yield from nodes

        edges_by_subject = {}
        for edge in self.__generate_kg_edges(nodes=nodes):
            edges_by_subject.setdefault(edge.subject, []).append(edge)
            yield edge

        paths = tuple(
            self.__generate_kg_paths(edges_by_subject=edges_by_subject, nodes=nodes)
        )
        yield from paths

        yield from self.__generate_benchmarks(paths=paths)

    def __generate_benchmarks(
        self, *, paths: Tuple[KgPath, ...]
    ) -> Generator[Model, None, None]:
        dataset_types = ("dev", "test", "train")
        prompt_types = list(BenchmarkQuestionPromptType)
        choice_types = list(BenchmarkQuestionChoiceType)

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
                    prompt_type = prompt_types[question_i % len(prompt_types)]
                    choice_type = choice_types[question_i % len(choice_types)]
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
                        concept=concepts[question_i % len(concepts)],
                        correct_choice_id=choices[question_i % len(choices)].id,
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
                            path = paths[question_i * path_i % len(paths)].path
                            question_answer_paths.append(
                                BenchmarkQuestionAnswerPaths(
                                    start_node_id=path[0],
                                    end_node_id=path[-1],
                                    score=path_i * 0.20,
                                    paths=(
                                        BenchmarkQuestionAnswerPath(
                                            path=path, score=path_i * 0.15
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
                        choice_id=question.choices[question_i % len(question.choices)].id,
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

    def __generate_kg_edges(
        self, nodes: Tuple[KgNode, ...]
    ) -> Generator[KgEdge, None, None]:
        concept_net_predicates = tuple(
            getattr(mowgli_etl.model.concept_net_predicates, attr)
            for attr in dir(mowgli_etl.model.concept_net_predicates)
            if not attr.startswith("_")
        )

        edge_set = MemKgEdgeSet()
        object_node_ids = MemIdSet()
        for subject_node_i, subject_node in tqdm(enumerate(nodes)):
            out_degree = subject_node_i % len(nodes)
            while out_degree < 10 or out_degree > 30:
                out_degree = (out_degree + 1) % len(nodes)
            for edge_i in range(out_degree):
                while True:
                    try_node_i = subject_node_i % len(nodes)
                    object_node = nodes[try_node_i]
                    while object_node.id == subject_node.id:
                        try_node_i = (try_node_i + 1) % len(nodes)
                        object_node = nodes[try_node_i]
                    predicate = concept_net_predicates[edge_i % len(concept_net_predicates)]
                    edge = KgEdge.with_generated_id(
                        object=object_node.id,
                        labels=(f"Test edge label {edge_i}",),
                        predicate=predicate,
                        subject=subject_node.id,
                        # sources=tuple(sorted(set(list(subject_node.sources) + list(object_node.sources)))),
                        sources=subject_node.sources,
                        # weight=floor(random.random() * 100.0) / 100.0,
                    )
                    if edge in edge_set:
                        continue
                    yield edge
                    edge_set.add(edge)
                    object_node_ids.add(edge.object)
                    break
        for node in nodes:
            if node.id not in object_node_ids:
                raise AssertionError(f"{node.id} not an object of an edge")

    def __generate_kg_nodes(self) -> Tuple[KgNode, ...]:
        pos = ("a", "n", "r", "v")
        shared_labels = tuple(f"Shared node label {label_i}" for label_i in range(100))

        return tuple(
            KgNode(
                id=f"portal_test_data:{node_i}",
                labels=(shared_labels[node_i % len(shared_labels)], f"Test node {node_i}", f"KgNode{node_i}", f"NodeAlias{node_i}"),
                pos=pos[node_i % len(pos)],
                sources=(PortalTestDataPipeline.ID, self.__SECONDARY_SOURCES[node_i % len(self.__SECONDARY_SOURCES)]),
            )
            for node_i in range(200)
        )

    def __generate_kg_paths(
        self, *, edges_by_subject: Dict[str, List[KgEdge]], nodes: Tuple[KgNode, ...]
    ) -> Generator[KgPath, None, None]:
        for path_i in range(10):
            current_node_id = start_node_id = nodes[path_i * 5 % len(nodes)].id
            path_length = path_i + 1  # expo_int(max=10, min=2, mean=4)
            path_node_ids = set(start_node_id)
            path = [start_node_id]
            # print("Start:", current_node_id)
            for link_i in range(path_length):
                current_node_edges = edges_by_subject[current_node_id]
                for try_edge_i in range(len(current_node_edges)):
                    choose_edge = current_node_edges[(path_i * link_i + try_edge_i) % len(current_node_edges)]
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
