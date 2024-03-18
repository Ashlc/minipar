import json
class SyntaxNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.scope = None
        self.nparams = None
        self.children = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def set_scope(self, scope):
        self.scope = scope

    def set_nparams(self, nparams):
        self.nparams = nparams

    def print_tree(self, level=0):
        indent = "    " * level
        print(f'{indent}{self.node_type} of value {self.value if self.value else "--"}')

        for child in self.children:
            child.print_tree(level + 1)