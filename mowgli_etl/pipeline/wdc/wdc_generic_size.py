from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions


@dataclass_json
@dataclass
class WdcGenericSize:
    name: str
    dimension: WdcProductDimensions
    count: int
    unit: str
    bucket: Optional[int] = None
