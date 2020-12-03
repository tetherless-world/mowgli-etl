from typing import Tuple
from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_generic_size import WdcGenericSize

class WdcSizeBuckets:
	def __init__(self):
		self.buckets = dict()

	def self.__bucket(self, dimension):
		# Determine heuristics for buckets
		pass

	def __convert(self, dimension, origin):
		if origin in ("in","lb","lbs","v",):
			return dimension
		if origin == "mm":
			return dimension * 3.9
		if origin == "cm":
			return dimension * 0.39
		if origin == "m":
			return dimension * 0.0039
		if origin == "ft":
			return dimension * 12
		if origin == "mv":
			return dimension / 1000
		if origin == "kv":
			return dimension * 1000
		if origin == "oz":
			return dimension / 16
		if origin == "g":
			return dimension 0.0022046
		if origin == "mg":
			return dimension * 0.0000022046
		if origin == "kg":
			return dimension * 2.2046

	def generalize(self, wdc_product: Tuple[WdcProductType, WdcProductDimensions]):
		# General units: in^3, V, lb
		product_type = wdc_product[0]
		product_dimensions = wdc_product[1]
		# Default spatial to in, power to V, weight to lb
		dimension = None
		unit = None
		if product_dimensions.depth or product_dimensions.height or product_dimensions.length or product_dimensions.width:
			dimension = dict()
			if product_dimensions.depth:
				dimension["depth"] = {"value": self.__convert(product_dimensions.depth.value, product_dimensions.depth.unit), "unit": "in"}
			if product_dimensions.height:
				dimension["height"] = {"value": self.__convert(product_dimensions.height.value, product_dimensions.height.unit), "unit": "in"}
			if product_dimensions.length:
				dimension["length"] = {"value": self.__convert(product_dimensions.length.value, product_dimensions.height.unit), "unit": "in"}
			if product_dimensions.width:
				dimension["width"] = {"value": self.__convert(product_dimensions.width.value, product_dimensions.width.unit), "unit": "in"}
			unit = "in^3"
		elif product_dimensions.power:
			dimension = {"value": self.__convert(product_dimensions.power.value, product_dimensions.power.unit), "unit": "V"}
			unit = "v'"
		elif product_dimensions.weight:
			dimension = {"value": self.__convert(product_dimensions.weight.value, product_dimensions.weight.unit), "unit": "lb"}
			unit = "lb"
		if not dimension:
			return None
		generic_dimensions = WdcGenericSize({"name": product_type.expected.name, "dimension": WdcProductDimensions.from_dict(dimension), "unit": unit})
		if product_type.expected.name in self.buckets:
			pass
		else:
			generic_dimensions.bucket = self.__bucket(generic_dimensions)
			self.buckets[product_type.expected.name] = generic_dimensions

		return generic_dimensions
