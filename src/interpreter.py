from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from _parser import Parser

class Interpreter:
    
    def __init__(self):
        pass  # Placeholder for interpreter initialization
    
    def interpret(self, syntax_tree):
        if syntax_tree.node_type == en.PROGRAM:
            for child in syntax_tree.children:
                self.execute_statement(child)
        else:
            raise Exception(f"Expected PROGRAM node at the root, got {syntax_tree.node_type}")
    
    def execute_declaration(self, node):
        if node.value[0][0] == en.RW_INT:
            identifier = node.value[0][1]
            value = 0  # Initialize integer variables with 0
            self.variables[identifier] = value
        else:
            raise NotImplementedError(f"Declaration type {node.value[0][0]} not implemented in interpreter.")

    def evaluate_expression(self, node):
        if node.node_type in (en.ID, en.NUM):
            return node.value
        elif node.node_type in (en.OP_PLUS, en.OP_MINUS, en.OP_MULTIPLY, en.OP_DIVIDE):
            left_value = self.evaluate_expression(node.children[0])
            right_value = self.evaluate_expression(node.children[1])
            if node.node_type == en.OP_PLUS:
                return left_value + right_value
            elif node.node_type == en.OP_MINUS:
                return left_value - right_value
            elif node.node_type == en.OP_MULTIPLY:
                return left_value * right_value
            else:
                return left_value / right_value
        elif node.node_type in (en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ):
            left_value = self.evaluate_expression(node.children[0])
            right_value = self.evaluate_expression(node.children[1])
            if node.node_type == en.OP_GT:
                return left_value > right_value
            elif node.node_type == en.OP_LT:
                return left_value < right_value
            elif node.node_type == en.OP_GE:
                return left_value >= right_value
            elif node.node_type == en.OP_LE:
                return left_value <= right_value
            else:
                return left_value == right_value
        else:
            raise Exception(f"Unsupported expression node type: {node.node_type}")

    def execute_statement(self, node):
        if node.node_type == en.OP_ASSIGN:
            identifier = node.children[0].value
            value = self.evaluate_expression(node.children[1])
            print(f"Assignment: {identifier} = {value}")  # Placeholder for variable storage
        elif node.node_type == en.RW_PRINT:
            value = self.evaluate_expression(node.children[0])
            print(value)
        elif node.node_type in (en.RW_IF, en.RW_WHILE, en.RW_FOR):
            self.execute_control_flow(node)
        else:
            raise Exception(f"Unsupported statement node type: {node.node_type}")

    def execute_control_flow(self, node):
        if node.node_type == en.RW_IF:
            condition = self.evaluate_expression(node.children[0])
            if condition:
                self.execute_statement(node.children[1])
            else:
                if len(node.children) == 3:
                    self.execute_statement(node.children[2])
        elif node.node_type == en.RW_WHILE:
            condition = self.evaluate_expression(node.children[0])
            while condition:
                self.execute_statement(node.children[1])
                condition = self.evaluate_expression(node.children[0])
        elif node.node_type == en.RW_FOR:
            initialization = node.children[0]
            self.execute_statement(initialization)

            condition = self.evaluate_expression(node.children[1])
            while condition:
                self.execute_statement(node.children[3])
                increment = node.children[2]
                self.execute_statement(increment)
                condition = self.evaluate_expression(node.children[1])
        else:
            raise Exception(f"Unsupported statement node type: {node.node_type}")


code = """
int x = 5;
int y = 6;
int z = x + y;

print(z);

if (x > y) {
    print("x is greater than y");
} else {
    print("y is greater than x");
}

while (x > 0) {
    print(x);
    x = x - 1;
}
"""

parser = Parser(code)
syntax_tree = parser.parse()

interpreter = Interpreter()

interpreter.interpret(syntax_tree)  # Execute the parsed syntax tree