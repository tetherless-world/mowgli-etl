from typing import NamedTuple, Tuple


class Path(NamedTuple):
    id: str
    # A sequence of subject, predicate, object/subject, predicate, object/subject, ..., object
    path: Tuple[str, ...]
