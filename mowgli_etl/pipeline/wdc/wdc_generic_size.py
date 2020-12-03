from dataclasses import dataclass
from typing import Optional
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions


@dataclass
class WdcGenericSize:
	name: str
	dimension: WdcProductDimensions
	unit: str
	bucket: Optional[int] = None
