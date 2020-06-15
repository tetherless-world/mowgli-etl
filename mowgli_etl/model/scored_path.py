from pathlib import Path
from typing import NamedTuple


class ScoredPath(NamedTuple):
    path: Path
    score: float
