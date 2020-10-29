from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class WdcProductDimensions:
    """
    Should we handle volume, mass dimensions?
    How do we handle multiple dimensions?
    How do we handle clothing dimensions?
    """

    @dataclass
    class __Dimension:
        value: Optional[float] = None
        unit: Optional[str] = None

    depth: Optional[__Dimension] = None
    height: Optional[__Dimension] = None
    length: Optional[__Dimension] = None
    width: Optional[__Dimension] = None
    power: Optional[__Dimension] = None
    weight: Optional[__Dimension] = None
