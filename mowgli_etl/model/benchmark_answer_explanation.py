from typing import NamedTuple, Tuple, Optional

from mowgli_etl.model.benchmark_question_choice_analysis import BenchmarkQuestionChoiceAnalysis


class BenchmarkAnswerExplanation(NamedTuple):
    choice_analyses: Optional[Tuple[BenchmarkQuestionChoiceAnalysis, ...]] = None
