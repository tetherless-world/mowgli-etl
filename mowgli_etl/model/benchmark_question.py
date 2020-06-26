from typing import NamedTuple, Optional, Tuple

from mowgli_etl.model.benchmark_question_choice import BenchmarkQuestionChoice
from mowgli_etl.model.benchmark_question_prompt import BenchmarkQuestionPrompt
from mowgli_etl.model.benchmark_question_type import BenchmarkQuestionType


class BenchmarkQuestion(NamedTuple):
    choices: Tuple[BenchmarkQuestionChoice, ...]
    id: str
    dataset_id: str
    prompts: Tuple[BenchmarkQuestionPrompt]
    categories: Optional[Tuple[str, ...]] = None
    concept: Optional[str] = None
    correct_choice_id: Optional[str] = None
    type: Optional[BenchmarkQuestionType] = BenchmarkQuestionType.MULTIPLE_CHOICE
