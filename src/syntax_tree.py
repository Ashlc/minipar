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

    def __str__(self):
        if self.value is not None:
            if isinstance(self.value, list):
                value_str = '[' + ', '.join(str(item) for item in self.value) + ']'
            else:
                value_str = str(self.value)
            return f"{self.node_type}: {value_str}"
        else:
            return self.node_type

    def print_tree(self, level=0):
        indent = "  " * level
        print(f'{indent}{str(self)}')

        for child in self.children:
            child.print_tree(level + 1)