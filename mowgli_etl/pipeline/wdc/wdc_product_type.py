from typing import NamedTuple, Optional, List


class WdcProductType(NamedTuple):
    name: str
    confidence: Optional[float] = None
    alternate: Optional[List[str]] = None
