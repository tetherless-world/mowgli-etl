from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_generic_size import WdcProductSize

from abc import ABC, abstractmethod
from dataclasses import fields


class WdcSizeBuckets(ABC):
    """
    Abstract structure for bucketing algorithms
    :param num_buckets: The maximum number of buckets that products will be sorted into. Default=5
    :param max_volume: The lower-bound on the largest bucket. Default=100,000
    """

    def __init__(self, *, num_buckets: int = 5, max_volume: float = 100000.0):
        self.averages = dict()
        self.max_volume = max_volume
        self.num_buckets = num_buckets

    @abstractmethod
    def generalize(
        self,
        *,
        wdc_product_type: WdcProductType,
        wdc_product_dimensions: WdcProductDimensions,
    ) -> WdcProductSize:
        """
        :param wdc_product_type: Parsed general product type
        :param wdc_product_dimensions: Parsed product dimensions
        :return: Generalized dimensions, not the average dimensions though
        """
