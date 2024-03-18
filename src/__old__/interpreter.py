from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from _parser import Parser

class Interpreter:
    
    def __init__(self):
        self.variables = {}
    
    def interpret(self, syntax_tree):
        
        if syntax_tree.node_type == en.PROGRAM:
            for child in syntax_tree.children:
                self.execute_statement(child)
        else:
            raise Exception(f"Expected PROGRAM node at the root, got {syntax_tree.node_type}")
    
    def execute_declaration(self, node):
        declaration_type = node.node_type
        print(f"Declaration type: {declaration_type}")  
        identifier = node.value.value[0][1]
        
        if declaration_type == en.RW_INT:
            value = node.value.value[1].value
        elif declaration_type == en.RW_BOOL:
            value = False  
        elif declaration_type == en.RW_STRING:
            value = ""  
        else:
            raise NotImplementedError(f"Declaration type {declaration_type} not implemented in interpreter.")

        self.variables[identifier] = value

    def evaluate_expression(self, node):
        if node.node_type in (en.ID, en.NUM):
            if node.node_type == en.ID:
                identifier = node.value
                if identifier in self.variables:
                    print(f"Variable '{identifier}' has value {self.variables[identifier]}")
                    return self.variables[identifier]
                else:
                    raise Exception(f"Variable '{identifier}' not defined.")
            else:  # Handle numeric literals
                return node.value
        elif node.node_type == en.STRING_LITERAL:
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
        if node.node_type == en.RW_PRINT: 
            value = self.evaluate_expression(node.value)
            print(value)
        elif node.node_type == en.RW_IF:
            self.execute_control_flow(node)
        elif node.node_type == en.RW_WHILE:
            self.execute_control_flow(node)
        elif node.node_type == en.RW_FOR:
            self.execute_control_flow(node)
        elif node.node_type in (en.RW_INT, en.RW_BOOL, en.RW_STRING):
            self.execute_declaration(node)
        elif node.node_type == en.BLOCK:
            print(node.value)
            self.execute_statement(node.value)
        elif node.value.node_type == en.OP_ASSIGN:
            op_node = node.value 
            print(f"OPNODE: {op_node.value}")
            identifier = op_node.value[0][1]
            value = self.evaluate_expression(op_node.value[1])
            print(f"Identifier: {identifier}, Value: {value}")
            self.variables[identifier] = value
            print(f"Assignment: {identifier} = {value}")
        else:
            raise Exception(f"Unsupported statement node type: {node.node_type}")
        
    def execute_control_flow(self, node):
        print(f"Executing if statement: {node}")
        if node.node_type == en.RW_IF:
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
int x = 30;
int y = 20;
int z = x + y;

print(z);

if (x > y) {
    print("x is greater than y");
} else {
    print("y is greater than x");
}
"""

parser = Parser(code)
syntax_tree = parser.parse() 

interpreter = Interpreter()

interpreter.interpret(syntax_tree)  