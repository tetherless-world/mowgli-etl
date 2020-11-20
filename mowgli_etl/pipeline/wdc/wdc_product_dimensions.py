from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


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
        """

        if self.weight is None:
            return 0
        return weight if self.weight.unit else weight / 2

    def __power_accuracy(self, weight: float) -> float:
        """
        Calculate power accuracy dependent on whether or not there's a unit associated
        """

        if self.power is None:
            return 0
        return weight if self.power.unit else weight / 2

    def accuracy(self, weight: float) -> float:
        """
        Calculate overall accuracy of the parsed dimension
        Parameters: weight - float associated to the source certainty
        Return: float - certainty of dimension
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
