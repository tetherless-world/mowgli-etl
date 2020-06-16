import bz2
import json

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.benchmark import Benchmark
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_answer_explanation import BenchmarkAnswerExplanation
from mowgli_etl.model.benchmark_question import BenchmarkQuestion

from mowgli_etl.model.benchmark_question_answer_path import BenchmarkQuestionAnswerPath
from mowgli_etl.model.benchmark_question_answer_paths import BenchmarkQuestionAnswerPaths
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_choice_analysis import BenchmarkQuestionChoiceAnalysis
from mowgli_etl.model.benchmark_question_set import BenchmarkQuestionSet
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.path import Path


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
        question_set_type = "dev"
        question_set_id = f"{benchmark_id}-{question_set_type}"
        yield \
            Benchmark(
                id=benchmark_id,
                name="CommonsenseQA",
                question_sets=(
                    BenchmarkQuestionSet(
                        id=question_set_id,
                        name=f"CommonsenseQA {question_set_type} set"
                    ),
                )
            )

        submission_id = f"kagnet-{question_set_id}"
        yield \
            BenchmarkSubmission(
                benchmark_id=benchmark_id,
                id=submission_id,
                question_set_id=question_set_id
            )

        with bz2.open(jsonl_bz2_file_path) as jsonl_bz2_file:
            for line in jsonl_bz2_file:
                obj = json.loads(line)
                question_obj = obj["question"]
                question_id = question_set_id + "-" + obj["id"]
                yield \
                    BenchmarkQuestion(
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
                yield \
                    BenchmarkAnswer(
                        choice_label=obj["chosenAnswer"],
                        explanation=BenchmarkAnswerExplanation(
                            choice_analyses=tuple(
                                BenchmarkQuestionChoiceAnalysis(
                                    choice_label=choice_obj["label"],
                                    question_answer_paths=tuple(
                                        BenchmarkQuestionAnswerPaths(
                                            end_node_id=explanation_obj["question_answer_concept_pair"][1],
                                            score=explanation_obj["pair_score"],
                                            start_node_id=explanation_obj["question_answer_concept_pair"][0],
                                            paths=tuple(
                                                BenchmarkQuestionAnswerPath(
                                                    path=tuple(path_component.rstrip('*') for path_component in path_obj["concept_relation_path"]),
                                                    score=path_obj["path_score"]
                                                )
                                                for path_obj in explanation_obj["paths"]
                                            )
                                        )
                                        for explanation_obj in choice_obj["explanation"]
                                    )
                                )
                                for choice_obj in question_obj["choices"]
                            )
                        ),
                        question_id=question_id,
                        submission_id=submission_id
                    )
