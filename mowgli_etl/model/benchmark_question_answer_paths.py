from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_question_answer_path import BenchmarkQuestionAnswerPath


class BenchmarkQuestionAnswerPaths(NamedTuple):
    start_node_id: str
    end_node_id: str
    paths: Tuple[BenchmarkQuestionAnswerPath, ...]
    score: float
