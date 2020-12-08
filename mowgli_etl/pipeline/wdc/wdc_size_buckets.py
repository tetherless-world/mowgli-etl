from typing import Tuple
from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_generic_size import WdcProductSize


class WdcSizeBuckets:
    def __init__(self):
        self.averages = dict()

    def __bucket(self, dimension):
        # Determine heuristics for buckets
        return None

    def generalize(
        self,
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

        if not wdc_product_type or not wdc_product_dimensions:
            return None

        generalized_dimensions = wdc_product_dimensions.to_english()

        unit = None

        for field in generalized_dimensions.keys():
            origin = getattr(generalized_dimensions, field.name)
            if origin and origin.unit:
                unit = origin.unit

        generic_dimensions = WdcProductSize(
            {
                "name": wdc_product_type.expected.name,
                "dimension": generalized_dimensions,
                "count": 1,
                "unit": unit,
            }
        )

        if generic_dimensions.name in self.averages:
            tracked_dimension = self.averages[generic_dimensions.name]
            for field in tracked_dimension.dimension.keys():
                tracked_dimension = getattr(tracked_dimension.dimension, field.name)
                new_dimension = getattr(generic_dimensions.dimension, field.name)

                # If the average dimension doesn't have the field, but the new dimension does, assign to new dimension
                if not dimension:
                    if not new_dimension:
                        continue
                    tracked_dimension.value = new_dimension.value
                    continue

                # If the field is not in the new dimension, set to average dimension
                if not new_dimension:
                    new_dimension = tracked_dimension.value
                else:
                    new_dimension = new_dimension.value

                tracked_dimension.value = (
                    dimension.value * tracked_dimension.count + new_dimension
                ) / (tracked_dimension.count + 1)
            tracked_dimension.count += 1

        else:
            self.averages[generic_dimensions.name] = generic_dimensions

        self.averages[generic_dimensions.name].bucket = self.__bucket(
            self.averages[generic_dimensions.name]
        )

        return generic_dimensions
