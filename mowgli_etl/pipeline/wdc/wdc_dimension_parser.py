from abc import ABC, abstractmethod


from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions


class WdcDimensionParser(ABC):
    @abstractmethod
    def parse(self, *, information: dict) -> WdcProductDimensions:
        """
        Parse product description to find dimensions
        """
