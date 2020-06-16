from typing import NamedTuple, Optional

from mowgli_etl.model.benchmark_answer_explanation import BenchmarkAnswerExplanation


class BenchmarkAnswer(NamedTuple):
    choice_label: str
    question_id: str
    submission_id: str
    explanation: Optional[BenchmarkAnswerExplanation] = None
