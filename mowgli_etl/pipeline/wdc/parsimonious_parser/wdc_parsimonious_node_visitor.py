from parsimonious.nodes import NodeVisitor


class WdcParsimoniousNodeVisitor(NodeVisitor):
    def __init__(self):
        self.dictionary = {}

    def visit_dimension(self, node, visited_children):
        entries = node.text.split(" ")
        value = ".".join(entries[0:-1])
        key = entries[-1]
        if key=='l':
        	key = 'length'
        elif key=='d':
        	key = 'depth'
        elif key=='w':
        	key = 'width'
        elif key=='h':
        	key = 'height'
        self.dictionary[key] = float(value)

    def visit_unit(self, node, visited_children):
        self.dictionary["unit"] = node.text

    def generic_visit(self, node, visited_children):
        return None
