from parsimonious.nodes import NodeVisitor

from dataclasses import dataclass, fields
from typing import Optional

class WdcParsimoniousNodeVisitor(NodeVisitor):

    @dataclass(frozen=True)
    class __Node:
        @dataclass
        class __Entry:
            value: Optional[float] = None
            unit: Optional[str] = None
        width: Optional[__Entry] = __Entry()
        depth: Optional[__Entry] = __Entry()
        height: Optional[__Entry] = __Entry()
        length: Optional[__Entry] = __Entry()

    def __init__(self):
        self.dictionary = WdcParsimoniousNodeVisitor.__Node()

    def reset(self):
        for key in fields(self.dictionary):
                getattr(self.dictionary, key.name).value = None
                getattr(self.dictionary, key.name).unit = None

    def visit_dimension(self, node, visited_children):
        entries = node.text.split(" ")
        value = ".".join(entries[0:-1])
        key = entries[-1]
        if key == "l":
            key = "length"
        elif key == "d":
            key = "depth"
        elif key == "w":
            key = "width"
        elif key == "h":
            key = "height"
        self.dictionary.__getattribute__(key).value = float(value)

    def visit_unit(self, node, visited_children):
        value = node.text.split(" ")[-1]
        for key in fields(self.dictionary):
        	getattr(self.dictionary, key.name).unit = value

    def generic_visit(self, node, visited_children):
        return None
