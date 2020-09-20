from typing import NamedTuple, Optional


class WdcProductDimensions(NamedTuple):
    """
    Should we handle volume, mass dimensions?
    How do we handle multiple dimensions?
    How do we handle clothing dimensions?
    """
    depth: Optional[float]
    height: Optional[float]
    length: Optional[float]
    width: Optional[float]
    unit: Optional[str]
