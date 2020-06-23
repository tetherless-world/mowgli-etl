import json
from pathlib import Path
from typing import Generator

from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.benchmark_question import BenchmarkQuestion
from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.model import Model


class McsBenchmarkTransformer(_Transformer):
    _TYPE = "@type"
    _LIST = "itemListElement"
    _QUESTION_TYPES = {"BenchmarkGoal", "BenchmarkQuestion", "BenchmarkObservation"}
    _CORRECT_CHOICE_LABEL = "correctChoiceLabel"

    def transform(self, benchmark_sample_path: Path) -> Generator[Model, None, None]:
        with open(benchmark_sample_path) as benchmark_sample_file:
            for json_txt in benchmark_sample_file.readlines():
                benchmark_sample = json.loads(json_txt)
                question_text = ""
                for antecedent_item in benchmark_sample["antecedent"][self._LIST]:
                    antecedent_type = antecedent_item[self._TYPE]
                    if antecedent_type in self._QUESTION_TYPES:
                        question_text += antecedent_item["text"]
                correct_choice_label = None
                if self._CORRECT_CHOICE_LABEL in benchmark_sample:
                    correct_choice_label = benchmark_sample[self._CORRECT_CHOICE_LABEL]

                choices = tuple(
                    BenchmarkQuestionChoice(label=choice["name"], text=choice["text"])
                    for choice in benchmark_sample["choices"][self._LIST]
                )

                yield BenchmarkQuestion(
                    id=benchmark_sample["@id"],
                    dataset_id=benchmark_sample["includedInDataset"],
                    text=question_text,
                    correct_choice_label=correct_choice_label,
                    choices=choices
                )


