from typing import Optional, List
from dataclasses import dataclass
from collections import Counter

@dataclass
class WdcProductType:

	METHOD_CONFIDENCE = {"category": 1/2, "description": 1/10, "title": 1/4, "specTableContent": 1/3}

	@dataclass
	class __Option:
		name: str
		confidence: float
		method: str

	expected: Optional[__Option] = None
	possible: Optional[List[__Option]] = None
	key: str = None
	key_confidence: float = None
	source: str = None

	def __init__(self, *, options, source):
		self.possible = []
		name_counter = Counter()
		for n in options:
			self.possible.append(n)
			name_counter[n.name] += 1
		for n in options:
			n.confidence *= name_counter[n.name]
		self.expected = sorted(self.possible, key=lambda x: (x.confidence, len(x.name)), reverse=True)[0]
		self.source = source

	def option(name, confidence, method):
		return WdcProductType.__Option(name, confidence, method)

	def set_key(self, key):
		self.key = key
		self.key_confidence = WdcProductType.METHOD_CONFIDENCE[key]
