from typing import NamedTuple, Tuple

from mowgli_etl.model.benchmark_question_answer_node_pair import BenchmarkQuestionAnswerNodePair


class BenchmarkAnswerExplanation(NamedTuple):
    question_answer_node_pairs: Tuple[BenchmarkQuestionAnswerNodePair, ...]
