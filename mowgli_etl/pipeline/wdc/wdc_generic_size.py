from dataclasses import dataclass
from typing import Optional

@dataclass
class WdcGenericSize:
	@dataclass
	class _Dimension:
		value: float
		unit: str
		count: int = 1

	name: str
	volume: Optional[_Dimension] = None
	power: Optional[_Dimension] = None
	weight: Optional[_Dimension] = None
