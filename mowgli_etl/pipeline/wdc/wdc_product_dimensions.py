from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy

from dataclasses_json import dataclass_json
from dataclasses import fields


@dataclass_json
@dataclass(frozen=True)
class WdcProductDimensions:
    """
    Store product dimensions in a dataclass for easier access
    """

    @dataclass
    class __Dimension:
        """
        Store dimensions separately to encapsulate information for each dimension
        """

        value: Optional[float] = None
        unit: Optional[str] = None
        value_text: Optional[str] = None
        unit_text: Optional[str] = None

    depth: Optional[__Dimension] = None
    height: Optional[__Dimension] = None
    length: Optional[__Dimension] = None
    width: Optional[__Dimension] = None
    power: Optional[__Dimension] = None
    weight: Optional[__Dimension] = None

    def __weight_accuracy(self, weight: float) -> float:
        """
        Calculate weight accuracy dependent on whether or not there's a unit associated

        :param weight: weight from source to be applied to dimension confidence
        :return: confidence of dimension result
        """

        if self.weight is None:
            return 0
        return weight if self.weight.unit else weight / 2

    def __power_accuracy(self, weight: float) -> float:
        """
        Calculate power accuracy dependent on whether or not there's a unit associated

        :param weight: weight from source to be applied to dimension confidence
        :return: confidence of dimension result
        """

        if self.power is None:
            return 0
        return weight if self.power.unit else weight / 2

    def accuracy(self, weight: float) -> float:
        """
        Calculate overall accuracy of the parsed dimension

        :param weight: weight from source to be applied to dimension confidence
        :return: confidence of dimension result
        """

        tally = 0
        for a in ("depth", "height", "length", "width"):
            if getattr(self, a) is not None:
                tally += 1
                if getattr(self, a).unit is not None:
                    tally += 1
        tally /= 6
        tally *= weight

        if tally == 0:
            ma = self.__weight_accuracy(weight)
            if ma != 0:
                return ma
            return self.__power_accuracy(weight)
        return tally

    def to_english(self):
        """
        Convert dimensions to english units (in, lb, lbs, v) in a new object
        """

        converter = {
            "mm": 3.9,
            "cm": 0.39,
            "m": 0.0039,
            "ft": 12,
            "mv": 1 / 1000,
            "kv": 1000,
            "oz": 1 / 16,
            "g": 0.0022046,
            "mg": 0.0000022046,
            "kg": 2.2046,
        }

        english_dimension = deepcopy(self)

        for field in fields(english_dimension):
            origin = getattr(english_dimension, field.name)
            if not origin:
                continue
            if origin.unit in (
                "in",
                "lb",
                "lbs",
                "v",
            ):
                continue
            if not origin.unit:
                if field.name in ("depth", "height", "width", "length"):
                    origin.unit = "in"
                elif field.name == "power":
                    origin.unit = "v"
                elif field.name == "weight":
                    origin.unit = "lbs"
                continue
            origin.value *= converter[origin.unit]

        return english_dimension
