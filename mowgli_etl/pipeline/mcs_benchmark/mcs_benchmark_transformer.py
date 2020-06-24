import json
from pathlib import Path
from typing import Dict, Generator, Tuple

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_choice_type import BenchmarkQuestionChoiceType
from mowgli_etl.model.benchmark_question_prompt import BenchmarkQuestionPrompt
from mowgli_etl.model.benchmark_question_prompt_type import BenchmarkQuestionPromptType
from mowgli_etl.model.benchmark_question_type import BenchmarkQuestionType
from mowgli_etl.model.benchmark_submission import BenchmarkSubmission
from mowgli_etl.model.model import Model


class McsBenchmarkTransformer(_Transformer):
    __TYPE = "@type"
    __LIST = "itemListElement"
    __CORRECT_CHOICE_LABEL = "correctChoiceLabel"
    __QUESTION_CHOICE_TYPE_DICT = {
        "BenchmarkAnswer": BenchmarkQuestionChoiceType.ANSWER,
        "BenchmarkHypothesis": BenchmarkQuestionChoiceType.HYPOTHESIS,
        "BenchmarkSolution": BenchmarkQuestionChoiceType.SOLUTION,
    }
    __QUESTION_PROMPT_TYPE_DICT = {
        "BenchmarkGoal": BenchmarkQuestionPromptType.GOAL,
        "BenchmarkObservation": BenchmarkQuestionPromptType.OBSERVATION,
        "BenchmarkQuestion": BenchmarkQuestionPromptType.QUESTION,
    }
    __QUESTION_TYPE_DICT = {
        "multiple choice": BenchmarkQuestionType.MULTIPLE_CHOICE,
        "true/false": BenchmarkQuestionType.TRUE_FALSE,
    }

    def __init__(self):
        super().__init__()
        self.__transformers = {
            "BenchmarkSample": self.__transform_benchmark_sample,
            "Submission": self.__transform_submission,
            "SubmissionSample": self.__transform_submission_sample,
        }

    def transform(
        self, benchmark_jsonl_paths: Tuple[Path]
    ) -> Generator[Model, None, None]:
        for jsonl_path in benchmark_jsonl_paths:
            with open(jsonl_path) as jsonl_file:
                for line in jsonl_file.readlines():
                    resource = json.loads(line)
                    resource_type = resource[self.__TYPE]
                    transformer = self.__transformers.get(resource_type)
                    if transformer is None:
                        raise ValueError(f"Unhandled top level type: {resource_type}")
                    yield from transformer(resource)

    def __transform_benchmark_sample(
        self, benchmark_sample_json
    ) -> Generator[BenchmarkQuestion, None, None]:
        prompts = []
        categories = None
        concept = None
        question_type = BenchmarkQuestionType.MULTIPLE_CHOICE
        for antecedent_item in benchmark_sample_json["antecedent"][self.__LIST]:
            antecedent_type = antecedent_item[self.__TYPE]
            if antecedent_type in self.__QUESTION_PROMPT_TYPE_DICT:
                prompts.append(
                    BenchmarkQuestionPrompt(
                        type=self.__QUESTION_PROMPT_TYPE_DICT[antecedent_type],
                        text=antecedent_item["text"],
                    )
                )
            elif antecedent_type == "BenchmarkQuestionCategory":
                categories = tuple(antecedent_item["text"])
            elif antecedent_type == "BenchmarkQuestionConcept":
                concept = antecedent_item["text"]
            elif antecedent_type == "BenchmarkQuestionType":
                question_type_val = antecedent_item["text"]
                assert (
                    question_type_val in self.__QUESTION_TYPE_DICT
                ), f"Unknown question type {question_type_val}"
                question_type = self.__QUESTION_TYPE_DICT[question_type_val]

        correct_choice_label = None
        if self.__CORRECT_CHOICE_LABEL in benchmark_sample_json:
            correct_choice_label = benchmark_sample_json[self.__CORRECT_CHOICE_LABEL]

        choices = tuple(
            BenchmarkQuestionChoice(
                label=choice["name"],
                text=choice["text"],
                type=self.__QUESTION_CHOICE_TYPE_DICT[choice[self.__TYPE]],
            )
            for choice in benchmark_sample_json["choices"][self.__LIST]
        )

        yield BenchmarkQuestion(
            id=benchmark_sample_json["@id"],
            dataset_id=benchmark_sample_json["includedInDataset"],
            categories=categories,
            concept=concept,
            choices=choices,
            correct_choice_label=correct_choice_label,
            prompts=tuple(prompts),
            type=question_type,
        )

    def __transform_submission(
        self, submission_sample_json
    ) -> Generator[BenchmarkSubmission, None, None]:
        yield from []

    def __transform_submission_sample(
        self, submission_sample_json
    ) -> Generator[BenchmarkAnswer, None, None]:
        yield from []
