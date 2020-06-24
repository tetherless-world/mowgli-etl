from typing import NamedTuple

from mowgli_etl.model.benchmark_question_prompt_type import BenchmarkQuestionPromptType


class BenchmarkQuestionPrompt(NamedTuple):
    text: str
    type: BenchmarkQuestionPromptType
