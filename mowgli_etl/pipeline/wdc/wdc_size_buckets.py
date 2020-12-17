from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_generic_size import WdcProductSize

from abc import ABC, abstractmethod
from dataclasses import fields

class WdcSizeBuckets(ABC):
    def __init__(self, *, num_buckets: int = 5, max_volume: float = 100000.):
        self.averages = dict()
        self.max_volume = max_volume
        self.num_buckets = num_buckets

    @abstractmethod
    def generalize(
        self,
        *,
        wdc_product_type: WdcProductType,
        wdc_product_dimensions: WdcProductDimensions,
    ):
        """
        :param wdc_product_type: Parsed general product type
        :type wdc_product_type: class<WdcProductType>
        :param wdc_product_dimensions: Parsed product dimensions
        :type wdc_product_dimensions: class<WdcProductDimensions>
        :return: Generalized dimensions, not the average dimensions though
        :rtype: class<WdcProductSize>
        """

