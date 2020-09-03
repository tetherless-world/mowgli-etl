from typing import NamedTuple

class ProductType(NamedTuple):
	name: str
	confidence : float

	def classify(self, *, title : str) -> ProductType:
		'''
		Parse title/listing/other to pull ProductType with confidence value
		'''
