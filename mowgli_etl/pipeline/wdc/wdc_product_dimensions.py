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

    depth: Optional[float] = None
    height: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    volume: Optional[float] = None
    mass: Optional[float] = None
    depth_unit: Optional[str] = None
    height_unit: Optional[str] = None
    length_unit: Optional[str] = None
    width_unit: Optional[str] = None
    volume_unit: Optional[str] = None
    mass_unit: Optional[str] = None
