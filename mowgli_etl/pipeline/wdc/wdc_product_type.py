from typing import NamedTuple, Optional


class WdcProductType(NamedTuple):
    name: str
    confidence: Optional[float] = None
