from typing import NamedTuple, Optional

class Dimension(NamedTuple):
	depth : Optional[float]
	height : Optional[float]
	length : Optional[float]
	width : Optional[float]

	def parse(self, *, description : str) -> Dimension:
		'''
		Parse description for dimension data. Return dimension namedtuple
		'''
