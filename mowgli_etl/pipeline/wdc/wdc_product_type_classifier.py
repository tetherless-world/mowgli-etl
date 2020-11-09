from abc import ABC, abstractmethod

from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry


class WdcProductTypeClassifier(ABC):
    @abstractmethod
    def classify(self, *, entry: WdcOffersCorpusEntry) -> WdcProductType:
        """
        Parse title/listing/other to pull ProductType with confidence value
        """
