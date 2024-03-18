from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from _parser import Parser

class Interpreter:
    
    def __init__(self):
        self.variables = {}
    
    def interpret(self, syntax_tree):
        # print(f"Interpreting syntax tree: {syntax_tree.node_type}")
        if syntax_tree.node_type == en.PROGRAM:
            for child in syntax_tree.children:
                self.execute_statement(child)
        else:
            raise Exception(f"Expected PROGRAM node at the root, got {syntax_tree.node_type}")
    
    def execute_declaration(self, node):
        print(f"Executing declaration: {node.node_type}")
        declaration_type = node.node_type
        identifier = node.value[0][1]
        print(f"NODE {node}, type {declaration_type}, identifier {identifier}")
        
        if declaration_type == en.RW_INT:
            value = 0  # Initialize integer variables with 0
        elif declaration_type == en.RW_BOOL:
            value = False  # Initialize boolean variables with False
        elif declaration_type == en.RW_STRING:
            value = ""  # Initialize string variables with an empty string
        else:
            raise NotImplementedError(f"Declaration type {declaration_type} not implemented in interpreter.")

        self.variables[identifier] = value

    def evaluate_expression(self, node):
        print(f"Evaluating expression: {node.node_type}")
        if node.node_type in (en.ID, en.NUM):
            return node.value
        elif node.node_type in (en.OP_PLUS, en.OP_MINUS, en.OP_MULTIPLY, en.OP_DIVIDE):
            
            left_value = self.evaluate_expression(node.value[0])
            right_value = self.evaluate_expression(node.value[1])
            if node.node_type == en.OP_PLUS:
                return left_value + right_value
            elif node.node_type == en.OP_MINUS:
                return left_value - right_value
            elif node.node_type == en.OP_MULTIPLY:
                return left_value * right_value
            else:
                return left_value / right_value
        elif node.node_type in (en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ):
            left_value = self.evaluate_expression(node.value[0])
            right_value = self.evaluate_expression(node.value[1])
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
            raise Exception(f"[evaluate_expression] Unsupported expression node type: {node.node_type}")

    def execute_statement(self, node):
        print(f"Executing statement: {node.node_type}")

        if node.node_type == en.OP_ASSIGN:
            # Handle assignment operation
            identifier = node.value[0].value
            
            value = self.evaluate_expression(node.value[1])
            print(f"Assignment: {identifier} = {value}")  # Placeholder for variable storage
        elif node.node_type == en.RW_PRINT:
            # Handle print statement
            print("Printing:")
            value = self.evaluate_expression(node.value)
            print(value)
        elif node.node_type == en.RW_IF:
            # Handle if statement
            self.execute_control_flow(node)
        elif node.node_type == en.RW_WHILE:
            # Handle while loop
            self.execute_control_flow(node)
        elif node.node_type == en.RW_FOR:
            # Handle for loop
            self.execute_control_flow(node)
        elif node.node_type in (en.RW_INT, en.RW_BOOL, en.RW_STRING):
            # Handle variable declaration
            self.execute_declaration(node)
        elif node.node_type == en.BLOCK:
            # Handle block of statements
            for child in node.children:
                self.execute_statement(child)
        else:
            raise Exception(f"Unsupported statement node type: {node.node_type}")
        
    def execute_control_flow(self, node):
        print(f"Executing control flow: {node.node_type}")
        if node.node_type == en.RW_IF:
            print(f"Node value: {node.value}")
            condition = self.evaluate_expression(node.value[0])
            if condition:
                self.execute_statement(node.value[1])
            else:
                if len(node.value) == 3:
                    self.execute_statement(node.value[2])
        elif node.node_type == en.RW_WHILE:
            condition = self.evaluate_expression(node.value[0])
            while condition:
                self.execute_statement(node.value[1])
                condition = self.evaluate_expression(node.value[0])
        elif node.node_type == en.RW_FOR:
            initialization = node.value[0]
            self.execute_statement(initialization)

            condition = self.evaluate_expression(node.value[1])
            while condition:
                self.execute_statement(node.value[3])
                increment = node.value[2]
                self.execute_statement(increment)
                condition = self.evaluate_expression(node.value[1])
        else:
            raise Exception(f"Unsupported statement node type: {node.node_type}")


code = """

if (x > y) {
    print("x is greater than y");
} else {
    print("y is greater than x");
}
"""

# while (x > 0) {
#     print(x);
#     x = x - 1;
# }

parser = Parser(code)
syntax_tree = parser.parse()

syntax_tree.print_tree()  # Print the parsed syntax tree

interpreter = Interpreter()

interpreter.interpret(syntax_tree)  # Execute the parsed syntax tree