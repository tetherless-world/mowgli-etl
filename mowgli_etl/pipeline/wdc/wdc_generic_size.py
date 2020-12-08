from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions


@dataclass_json
@dataclass
class WdcProductSize:
    """
    :field name: Product type name pulled from WdcProductType.expected
    :type name: str
    :field dimension: Generic product dimensions
    :type dimension: class<WdcProductDimensions>
    :field count: Number of WdcProducts used to calculate dimension. Used for updating the generic size if a new product is found
    :type count: int
    :field unit: Unit of measurement for the dimension. Separated from dimension for parsing purposes
    :type unit: str
    :field bucket: The size bucket the product fits in. Defautl=None
    :type bucket: int
    """

    name: str
    dimension: WdcProductDimensions
    count: int
    unit: str
    bucket: Optional[int] = None
