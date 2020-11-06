from typing import Optional, List
from dataclasses import dataclass

@dataclass
class WdcProductType:

	@dataclass
	class __Option:
		name: str
		confidence: float
		method: str

	expected: Optional[__Option] = None
	possible: Optional[List[__Option]] = None
	source: str = None

	def __init__(self, *, options, source):
		self.possible = []
		for n in options:
			self.possible.append(n)
		self.expected = sorted(self.possible, key=lambda x: (x.confidence, len(x.name)), reverse=True)[0]
		self.source = source

	def option(name, confidence, method):
		return WdcProductType.__Option(name, confidence, method)
