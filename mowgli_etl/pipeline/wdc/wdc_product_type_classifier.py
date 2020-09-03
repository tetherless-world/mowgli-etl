from abc import ABC, abstractmethod

from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType


class WdcProductTypeClassifier(ABC):
    @abstractmethod
    def classify(self, *, title: str) -> WdcProductType:
        '''
        Parse title/listing/other to pull ProductType with confidence value
        '''
