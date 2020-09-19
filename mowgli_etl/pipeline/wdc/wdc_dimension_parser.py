from abc import ABC, abstractmethod


from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions

class WdcDimensionParser(ABC)
    @abstractmethod
    def parse(self,*,description:str) -> WdcProductDimensions:
        """
        Parse product description to find dimensions
        """
