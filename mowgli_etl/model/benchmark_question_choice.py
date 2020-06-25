from typing import NamedTuple, Optional

from mowgli_etl.model.benchmark_question_choice_type import BenchmarkQuestionChoiceType


class BenchmarkQuestionChoice(NamedTuple):
    id: str
    position: int
    text: str
    type: BenchmarkQuestionChoiceType
    identifier: Optional[str] = None
