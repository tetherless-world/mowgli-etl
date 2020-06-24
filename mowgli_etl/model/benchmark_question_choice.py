from typing import NamedTuple, Optional

from mowgli_etl.model.benchmark_question_choice_type import BenchmarkQuestionChoiceType


class BenchmarkQuestionChoice(NamedTuple):
    label: str
    text: str
    type: BenchmarkQuestionChoiceType
