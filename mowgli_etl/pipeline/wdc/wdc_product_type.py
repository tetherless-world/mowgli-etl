from typing import Optional, List
from dataclasses import dataclass
from collections import Counter


@dataclass(init=False)
class WdcProductType:

    METHOD_CONFIDENCE = {
        "category": 1 / 2,
        "description": 1 / 10,
        "title": 1 / 4,
        "spec_table_content": 1 / 3,
        None: 0,
    }

    @dataclass
    class __Option:
        name: str
        confidence: float
        method: str

    expected: Optional[__Option] = None
    possible: Optional[List[__Option]] = None
    key: str = None
    key_confidence: float = None
    source: str = None

    def __init__(self, *, options, source, key):
        self.possible = []
        if options:
            name_counter = Counter()
            for n in options:
                self.possible.append(WdcProductType.__Option(n[0], n[1], n[2]))
                name_counter[n[0]] += 1
            for n in self.possible:
                n.confidence *= name_counter[n.name]
            self.expected = sorted(
                self.possible, key=lambda x: (x.confidence, len(x.name)), reverse=True
            )[0]

        self.source = source
        self.key = key
        self.key_confidence = WdcProductType.METHOD_CONFIDENCE[key]
