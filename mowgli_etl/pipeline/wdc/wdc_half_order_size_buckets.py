from mowgli_etl.pipeline.wdc.wdc_size_buckets import WdcSizeBuckets
from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_generic_size import WdcProductSize

from dataclasses import fields


class WdcHalfOrderSizeBuckets(WdcSizeBuckets):
    """
    Implementation of WdcSizeBuckets that uses half orders of magnitude for bucketing
    """

    def __bucket(self, dimension):
        # Determine heuristics for buckets
        # Assume that any None dimension is 1
        """
        depth:
            min: 6.0
            max: 64.0
        height:
            min: 3.0
            max: 11.0
        length:
            min: 0.12
            max: 38.0
        width:
            min: 1.3
            max: 34.0

        volume:
            min: 0.468
            max: 82,688

        Buckets:
            1: 0
            2:
            3:
            4:
            5: 100,000
        """
        # bucket_1 = 0
        # bucket_2 = 100000 * (10 ** (1 / 4)) / 10
        # bucket_3 = 100000 * (10 ** (1 / 2)) / 10
        # bucket_4 = 100000 * (10 ** (3 / 4)) / 10
        # bucket_5 = 100000
        volume = -1
        for field in ("depth", "height", "length", "width"):
            dim = getattr(dimension.dimension, field)
            if not dim:
                continue
            if volume < 0:
                volume = dim.value
            else:
                volume *= dim.value

        dimension.volume = volume

        for i in range(self.num_buckets - 1, 0, -1):
            if volume >= self.max_volume * (10 ** (i / (self.num_buckets - 1))) / 10:
                return i + 1
        if volume >= 0:
            return 1

        return None

    def generalize(
        self,
        *,
        wdc_product_type: WdcProductType,
        wdc_product_dimensions: WdcProductDimensions
    ) -> WdcProductSize:
        if not wdc_product_type or not wdc_product_dimensions:
            return None

        generalized_dimensions = wdc_product_dimensions.to_english()

        unit = None

        for field in fields(generalized_dimensions):
            origin = getattr(generalized_dimensions, field.name)
            if origin and origin.unit:
                unit = origin.unit

        generic_dimensions = WdcProductSize.from_dict(
            {
                "name": wdc_product_type.expected.name,
                "dimension": generalized_dimensions,
                "count": 1,
                "unit": unit,
            }
        )

        if generic_dimensions.name in self.averages:
            tracked_dimension = self.averages[generic_dimensions.name]
            for field in fields(tracked_dimension.dimension):
                old_dimension = getattr(tracked_dimension.dimension, field.name)
                new_dimension = getattr(generic_dimensions.dimension, field.name)

                # If the average dimension doesn't have the field, but the new dimension does, assign to new dimension
                if not old_dimension:
                    if not new_dimension:
                        continue
                    old_dimension = new_dimension
                if not new_dimension:
                    continue

                # If the field is not in the new dimension, set to average dimension
                if not new_dimension:
                    new_dimension = old_dimension.value
                else:
                    new_dimension = new_dimension.value

                old_dimension.value = (
                    old_dimension.value * tracked_dimension.count + new_dimension
                ) / (tracked_dimension.count + 1)
            tracked_dimension.count += 1

        else:
            self.averages[generic_dimensions.name] = generic_dimensions

        self.averages[generic_dimensions.name].bucket = self.__bucket(
            self.averages[generic_dimensions.name]
        )

        return generic_dimensions
