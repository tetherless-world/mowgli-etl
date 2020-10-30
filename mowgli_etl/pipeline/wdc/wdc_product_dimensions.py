from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class WdcProductDimensions:
    """
    """

    @dataclass
    class __Dimension:
        value: Optional[float] = None
        unit: Optional[str] = None

    depth: Optional[__Dimension] = None
    height: Optional[__Dimension] = None
    length: Optional[__Dimension] = None
    width: Optional[__Dimension] = None
    power: Optional[__Dimension] = None
    weight: Optional[__Dimension] = None

    def __weight_accuracy(self, weight: float) -> float:
        if self.weight is None:
            return 0
        return weight if self.weight.unit else weight/2

    def __power_accuracy(self, weight: float) -> float:
        if self.power is None:
            return 0
        return weight if self.power.unit else weight/2

    def accuracy(self, weight: float) -> float:
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
