import bz2
import json

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_answer_explanation import BenchmarkAnswerExplanation
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_answer_node_pair import BenchmarkQuestionAnswerNodePair
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_set import BenchmarkQuestionSet
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.path import Path
from mowgli_etl.model.scored_path import ScoredPath


class PortalBenchmarkTransformer(_Transformer):
    def transform(self, *,
        kagnet_commonsenseqa_benchmark_submission_jsonl_bz2_file_path: Path,
        **kwds
    ):
        yield from \
            self.__transform_kagnet_commonsenseqa_benchmark_submission(
                jsonl_bz2_file_path=kagnet_commonsenseqa_benchmark_submission_jsonl_bz2_file_path
            )

    def __transform_kagnet_commonsenseqa_benchmark_submission(self, jsonl_bz2_file_path):
        benchmark_id = "commonsenseqa"
        yield \
            Benchmark(
                id=benchmark_id,
                name="CommonsenseQA"
            )

        question_set_id = "dev"
        yield \
            BenchmarkQuestionSet(
                benchmark_id=benchmark_id,
                id=question_set_id,
            )

        answers = []
        with bz2.open(jsonl_bz2_file_path) as jsonl_bz2_file:
            for line in jsonl_bz2_file:
                obj = json.loads(line)
                question_obj = obj["question"]
                question_id = obj["id"]
                yield \
                    BenchmarkQuestion(
                        benchmark_id=benchmark_id,
                        choices=tuple(
                            BenchmarkQuestionChoice(
                                label=choice_obj["label"],
                                text=choice_obj["text"],
                            )
                            for choice_obj in question_obj["choices"]
                        ),
                        concept=question_obj["question_concept"],
                        correct_choice_label=obj["answerKey"],
                        id=question_id,
                        question_set_id=question_set_id,
                        text=question_obj["stem"],
                    )
                # Combine explanations for all choices
                explanation_objs = []
                for choice_obj in question_obj["choices"]:
                    explanation_objs.extend(choice_obj["explanation"])
                answers.append(
                    BenchmarkAnswer(
                        choice_label=obj["chosenAnswer"],
                        explanation=BenchmarkAnswerExplanation(
                            question_answer_node_pairs=tuple(
                                BenchmarkQuestionAnswerNodePair(
                                    end_node_id=explanation_obj["question_answer_concept_pair"][1],
                                    paths=tuple(
                                        ScoredPath(
                                            path=Path(
                                                datasource=benchmark_id,
                                                id=f"{benchmark_id}-{question_set_id}-{question_id}-{explanation_i}-{path_i}",
                                                path=tuple(path_component.rstrip('*') for path_component in path_obj["concept_relation_path"]),
                                            ),
                                            score=path_obj["path_score"]
                                        )
                                        for path_i, path_obj in enumerate(explanation_obj["paths"])
                                    ),
                                    start_node_id=explanation_obj["question_answer_concept_pair"][0],
                                    score=explanation_obj["pair_score"]
                                )
                                for explanation_i, explanation_obj in enumerate(explanation_objs)
                            )
                        ),
                        question_id=question_id
                    )
                )
        yield \
            BenchmarkSubmission(
                benchmark_id=benchmark_id,
                question_set_id=question_set_id,
                answers=tuple(answers)
            )
