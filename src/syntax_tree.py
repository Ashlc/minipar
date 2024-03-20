from enum_tokens import TokenEnums as en
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
        print(
            f'{indent}{self.node_type} of value {self.value if self.value is not None else "--"}'
        )

        for child in self.children:
            child.print_tree(level + 1)

    def to_json(self):
        def convert_enum_to_str(value):
            if isinstance(value, en):
                return value.name
            return value

        node_json = {
            "node_type": convert_enum_to_str(self.node_type),
            "value": (
                self.value.to_json()
                if isinstance(self.value, SyntaxNode)
                else convert_enum_to_str(self.value) if self.value is not None else "--"
            ),
            "children": [child.to_json() for child in self.children],
        }
        return node_json

    def evaluate(self, indent_level=0):
        indent = "    " * indent_level
        if self.node_type == en.PROGRAM:
            code = ""
            for child in self.children:
                code += child.evaluate(indent_level) + "\n"
            return code
        if self.node_type == en.RW_INT:
            output = ""
            for child in self.children:
                output += child.evaluate(indent_level) + "\n"
            return output

        elif self.node_type == en.OP_ASSIGN:
            variable = self.children[0].value
            expression = self.children[1]
            return f"{variable} = {expression.evaluate()}"

        elif self.node_type == en.OP_PLUS:

            left = self.children[0].evaluate()
            right = self.children[1].evaluate()
            return f"({left} + {right})"

        elif self.node_type == en.ID:
            return self.value

        elif self.node_type == en.NUM:
            return str(self.value)

        elif self.node_type == en.STRING_LITERAL:
            return f'"{self.value}"'

        elif self.node_type == en.RW_FOR:
            init = self.children[0].evaluate(indent_level + 1)
            condition = self.value.evaluate()
            increment = self.children[1].evaluate(indent_level + 1)
            block = self.children[2].evaluate(indent_level + 1)
            return f"{indent}for {init}; {condition}; {increment}:\n{block}"

        elif self.node_type == en.RW_IF:
            condition = self.value.evaluate()
            block_true = self.children[0].evaluate(indent_level + 1)
            block_false = self.children[1].evaluate(indent_level + 1)
            return f"{indent}if {condition}:\n{block_true}{indent}else:\n{block_false}"

        elif self.node_type == en.BLOCK:
            block_code = ""
            for child in self.children:
                block_code += child.evaluate(indent_level + 1) + "\n"
            return f"{indent}{block_code}"

        elif self.node_type == en.RW_PRINT:
            expression = self.children[0].evaluate()
            return f"{indent}print({expression})\n"

        elif self.node_type in [
            en.OP_GT,
            en.OP_LT,
            en.OP_GE,
            en.OP_LE,
            en.OP_EQ,
            en.OP_NE,
        ]:
            left = self.children[0].evaluate()
            right = self.children[1].evaluate()
            if self.node_type == en.OP_GT:
                return f"{left} > {right}"
            elif self.node_type == en.OP_LT:
                return f"{left} < {right}"
            elif self.node_type == en.OP_GE:
                return f"{left} >= {right}"
            elif self.node_type == en.OP_LE:
                return f"{left} <= {right}"
            elif self.node_type == en.OP_EQ:
                return f"{left} == {right}"
            elif self.node_type == en.OP_NE:
                return f"{left} != {right}"

        else:
            raise ValueError(f"Invalid node_type enum {self.node_type}")
