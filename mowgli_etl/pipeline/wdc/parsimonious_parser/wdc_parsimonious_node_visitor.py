from parsimonious.nodes import NodeVisitor


class WdcParsimoniousNodeVisitor(NodeVisitor):
    def __init__(self):
        self.dictionary = {}

    def visit_dimension(self, node, visited_children):
        value, key = node.text.split(" ")
        self.dictionary[key] = value

    def visit_unit(self, node, visited_children):
        self.dictionary["unit"] = node.text

    def generic_visit(self, node, visited_children):
        return None
