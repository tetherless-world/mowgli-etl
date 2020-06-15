from typing import NamedTuple, Optional, Tuple

from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice


class BenchmarkQuestion(NamedTuple):
    benchmark_id: str
    choices: Tuple[BenchmarkQuestionChoice, ...]
    concept: Optional[str]
    id: str
    text: str
