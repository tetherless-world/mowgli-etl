from parsimonious.nodes import NodeVisitor

from dataclasses import dataclass, fields
from typing import Optional


class WdcParsimoniousNodeVisitor(NodeVisitor):
    """
    NodeVisitor implementation for Wdc Parsimonious Grammar parsing
    """

    # Dictionary mapping a unit to a full-text unit
    COMMON_UNIT = ["l", "d", "w", "h"]
    KEY_MAP = {
        "l": "length",
        "d": "depth",
        "w": "width",
        "h": "height",
        "v": "power",
        "mv": "volatage",
        "kv": "power",
        "lb": "weight",
        "lbs": "weight",
        "oz": "weight",
        "g": "weight",
        "mg": "weight",
        "kg": "weight",
    }

    @dataclass
    class __Node:
        """
        Store information from each Node
        """

        @dataclass
        class Entry:
            """
            Store entry found from Node
            """

            value: Optional[float] = None
            unit: Optional[str] = None
            value_text: Optional[str] = None
            unit_text: Optional[str] = None

        width: Optional[Entry] = None
        depth: Optional[Entry] = None
        height: Optional[Entry] = None
        length: Optional[Entry] = None
        weight: Optional[Entry] = None
        power: Optional[Entry] = None

    def __init__(self):
        """
        Initialize dictionary as Node object
        """

        self.dictionary = WdcParsimoniousNodeVisitor.__Node()

    def __parse_decimal(self, values):
        """
        Parse decimal values by assuming a space between digits is a decimal
        """

        if len(values) == 0:
            return
        if len(values) == 1:
            return values[0]
        if len(values) == 2:
            return ".".join(values)
        return str(int(values[0]) + float(".".join(values[1:])))

    def visit_dimension(self, node, visited_children):
        """
        Parse dimension value into local dictionary
        """

        entries = node.text.split(" ")
        value = self.__parse_decimal(entries[0:-1])
        key = WdcParsimoniousNodeVisitor.KEY_MAP[entries[-1]]
        if getattr(self.dictionary, key) is None:
            setattr(self.dictionary, key, self.dictionary.Entry())
        getattr(self.dictionary, key).value = float(value)
        getattr(self.dictionary, key).value_text = node.text

    def visit_unit(self, node, visited_children):
        """
        Parse unit from unit dictionary
        """

        value = node.text.split(" ")[-1]
        if value in WdcParsimoniousNodeVisitor.COMMON_UNIT:
            for key in WdcParsimoniousNodeVisitor.COMMON_UNIT:
                if (
                    getattr(self.dictionary, WdcParsimoniousNodeVisitor.KEY_MAP[key])
                    is not None
                ):
                    getattr(
                        self.dictionary, WdcParsimoniousNodeVisitor.KEY_MAP[key]
                    ).unit = value
                    getattr(
                        self.dictionary, WdcParsimoniousNodeVisitor.KEY_MAP[key]
                    ).unit_text = node.text

    def visit_weight(self, node, visited_children):
        """
        Parse weight values
        """

        self.dictionary.source = node.text
        entries = node.text.split(" ")
        value = self.__parse_decimal(entries[0:-1])
        unit = entries[-1]
        self.dictionary.weight = self.dictionary.Entry()
        self.dictionary.weight.value = float(value)
        self.dictionary.weight.value_text = node.text
        self.dictionary.weight.unit = unit
        self.dictionary.weight.unit_text = node.text

    def visit_power(self, node, visited_children):
        """
        Parse power values
        """

        entries = node.text.split(" ")
        value = self.__parse_decimal(entries[0:-1])
        unit = entries[-1]
        self.dictionary.power = self.dictionary.Entry()
        self.dictionary.power.value = float(value)
        self.dictionary.power.value_text = node.text
        self.dictionary.power.unit = unit
        self.dictionary.power.unit_text = node.text

    def generic_visit(self, node, visited_children):
        """
        Catchall for unnamed grammar results
        """

        return None
