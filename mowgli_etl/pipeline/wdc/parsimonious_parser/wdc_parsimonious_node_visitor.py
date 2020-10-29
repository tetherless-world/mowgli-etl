from parsimonious.nodes import NodeVisitor

from dataclasses import dataclass, fields
from typing import Optional


class WdcParsimoniousNodeVisitor(NodeVisitor):
    KEY_MAP = {"l": "length", "d": "depth", "w": "width", "h": "height"}

    @dataclass
    class __Node:
        @dataclass
        class Entry:
            value: Optional[float] = None
            unit: Optional[str] = None

        width: Optional[Entry] = None
        depth: Optional[Entry] = None
        height: Optional[Entry] = None
        length: Optional[Entry] = None

    def __init__(self):
        self.dictionary = WdcParsimoniousNodeVisitor.__Node()

    def visit_dimension(self, node, visited_children):
        entries = node.text.split(" ")
        value = ".".join(entries[0:-1])
        key = WdcParsimoniousNodeVisitor.KEY_MAP[entries[-1]]
        if getattr(self.dictionary, key) is None:
            setattr(self.dictionary, key, self.dictionary.Entry())
        getattr(self.dictionary, key).value = float(value)

    def visit_unit(self, node, visited_children):
        value = node.text.split(" ")[-1]
        for key in fields(self.dictionary):
            if getattr(self.dictionary, key.name) is not None:
                getattr(self.dictionary, key.name).unit = value

    def generic_visit(self, node, visited_children):
        return None
