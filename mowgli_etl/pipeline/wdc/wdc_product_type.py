from typing import Optional, List
from dataclasses import dataclass

@dataclass
class WdcProductType:

	@dataclass
	class __Option:
		name: str
		confidence: float

	expected_name: Optional[__Option] = None
	possible_names: Optional[List[__Option]] = None
