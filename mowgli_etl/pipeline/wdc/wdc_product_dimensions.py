from typing import NamedTuple, Optional


class WdcProductDimensions(NamedTuple):
    depth: Optional[float]
    height: Optional[float]
    length: Optional[float]
    width: Optional[float]
