from typing import NamedTuple, Optional, Tuple

from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice


class BenchmarkQuestion(NamedTuple):
    choices: Tuple[BenchmarkQuestionChoice, ...]
    id: str
    dataset_id: str
    text: str
    concept: Optional[str] = None
    correct_choice_label: Optional[str] = None
