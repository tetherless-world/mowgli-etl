from typing import NamedTuple, Tuple

from mowgli_etl.model.scored_path import ScoredPath


class BenchmarkQuestionAnswerNodePair(NamedTuple):
    start_node_id: str
    end_node_id: str
    score: float
    paths: Tuple[ScoredPath, ...]
