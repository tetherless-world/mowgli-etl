import json
from pathlib import Path
from typing import Dict, Generator, Tuple

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.benchmark_answer import BenchmarkAnswer
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.model import Model


class McsBenchmarkTransformer(_Transformer):
    _TYPE = "@type"
    _LIST = "itemListElement"
    _QUESTION_TYPES = {"BenchmarkGoal", "BenchmarkQuestion", "BenchmarkObservation"}
    _CORRECT_CHOICE_LABEL = "correctChoiceLabel"

    def __init__(self):
        super().__init__()
        self.__transformers = {
            "BenchmarkSample": self.transform_benchmark_sample,
            "SubmissionSample": self.transform_submission_sample,
        }

    def transform(
        self, benchmark_jsonl_paths: Tuple[Path]
    ) -> Generator[Model, None, None]:
        for jsonl_path in benchmark_jsonl_paths:
            with open(jsonl_path) as jsonl_file:
                for line in jsonl_file.readlines():
                    resource = json.loads(line)
                    resource_type = resource[self._TYPE]
                    if resource_type not in self.__transformers:
                        raise ValueError(f"Unhandled top level type: {resource_type}")
                    transformer = self.__transformers[resource_type]
                    yield from transformer(resource)

    def transform_benchmark_sample(
        self, benchmark_sample_json
    ) -> Generator[BenchmarkQuestion, None, None]:
        question_text = ""
        for antecedent_item in benchmark_sample_json["antecedent"][self._LIST]:
            antecedent_type = antecedent_item[self._TYPE]
            if antecedent_type in self._QUESTION_TYPES:
                question_text += antecedent_item["text"]
        correct_choice_label = None
        if self._CORRECT_CHOICE_LABEL in benchmark_sample_json:
            correct_choice_label = benchmark_sample_json[self._CORRECT_CHOICE_LABEL]

        choices = tuple(
            BenchmarkQuestionChoice(label=choice["name"], text=choice["text"])
            for choice in benchmark_sample_json["choices"][self._LIST]
        )

        yield BenchmarkQuestion(
            id=benchmark_sample_json["@id"],
            dataset_id=benchmark_sample_json["includedInDataset"],
            text=question_text,
            correct_choice_label=correct_choice_label,
            choices=choices,
        )

    def transform_submission_sample(
        self, submission_sample_json
    ) -> Generator[BenchmarkAnswer, None, None]:
        yield from []
