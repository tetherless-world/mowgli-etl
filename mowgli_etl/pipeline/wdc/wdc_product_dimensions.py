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
    volume: Optional[float]
    mass: Optional[float]
    depth_unit: Optional[str]
    height_unit: Optional[str]
    length_unit: Optional[str]
    width_unit: Optional[str]
    volume_unit: Optional[str]
    mass_unit: Optional[str]
