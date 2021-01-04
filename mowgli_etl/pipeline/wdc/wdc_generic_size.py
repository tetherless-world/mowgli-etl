from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, Union
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions


@dataclass_json
@dataclass
class WdcProductSize:
    """
    :field name: Product type name pulled from WdcProductType.expected
    :field dimension: Generic product dimensions
    :field count: Number of WdcProducts used to calculate dimension. Used for updating the generic size if a new product is found
    :field unit: Unit of measurement for the dimension. Separated from dimension for parsing purposes
    :field bucket: The size bucket the product fits in. Default=None
    :field volume: The volume of the product. Default=None
    """

    name: str
    dimension: WdcProductDimensions
    count: int
    unit: str
    bucket: Optional[Union[int, float]] = None
    volume: Optional[float] = None
