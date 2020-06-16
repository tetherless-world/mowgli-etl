from typing import NamedTuple, Tuple

from mowgli_etl.model.scored_path import ScoredPath


class BenchmarkQuestionAnswerPaths(NamedTuple):
    start_node_id: str
    end_node_id: str
    paths: Tuple[ScoredPath, ...]
    score: float
