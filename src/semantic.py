from _parser import Parser
from enum_tokens import TokenEnums as en
from lexer import Lexer

class Semantics:
    def __init__(self):
        self.environments = [{}]
        self.types = [{}]

    def enter_scope(self):
        self.environments.append({})
        self.types.append({})

    def exit_scope(self):
        self.environments.pop()
        self.types.pop()

    def visit(self, node):
        method_name = f'visit_{node.node_type.name}'
        print(f"Visiting {node.node_type.name}")
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{node.node_type.name} method defined")

    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)

    def visit_children(self, node):
        for child in node.children:
            self.visit(child)

    def visit_RW_INT(self, node):
        self.current_type = 'RW_INT'
        self.visit_children(node)

    def visit_RW_BOOL(self, node):
        self.current_type = 'RW_BOOL'
        self.visit_children(node)

    def visit_RW_STRING(self, node):
        self.current_type = 'RW_STRING'
        self.visit_children(node)

    def visit_RW_C_CHANNEL(self, node):
        self.current_type = 'RW_C_CHANNEL'
        self.visit_children(node)
        
    def visit_RW_PRINT(self, node):
        value = self.visit(node.children[0])
        print(f"Printing: {value}")

    def visit_OP_ASSIGN(self, node):
        node.print_tree()
        if node.children:
            name = node.children[0].value  # Get the name from the identifier node
            print(f"Name: {name}")
            
            if node.children[1].value is not None:
                print(f"Value: {node.children[1].value}")
                value = self.visit(node.children[1])

            if name in self.types[-1] and self.types[-1][name] != self.current_type:
                raise Exception(f"Type error: variable '{name}' was declared as {self.types[-1][name]} but assigned a value of type {self.current_type}")

            print(f"Assigning {value} to {name}")
            
            self.environments[-1][name] = value
            self.types[-1][name] = self.current_type
        else:
            raise Exception("OP_ASSIGN node has no children")

    def visit_ID(self, node):
        node.print_tree()
        name = node.value  # Get the name from the ID node
        for env in reversed(self.environments):
            if name in env:
                return env[name]
        raise Exception(f"NameError: name '{name}' is not defined")

    def visit_NUM(self, node):
        return 'RW_INT'

    def visit_STRING_LITERAL(self, node):
        return 'RW_STRING'
    
    def visit_BLOCK(self, node):
        self.enter_scope()
        for statement_node in node.children:
            self.visit(statement_node)
        self.exit_scope()

    def visit_OP_PLUS(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        return "RW_INT"
    
    def visit_RW_WHILE(self, node):
        node.print_tree()
        condition_node = node.children[0]
        block_node = node.children[1]

        while self.visit(condition_node):
            self.visit(block_node)

    def visit_OP_MINUS(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        return "RW_INT"

    def visit_OP_GT(self, node):
        node.print_tree()
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_OP_LT(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_OP_GE(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_OP_LE(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")
        
    def visit_OP_EQ(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_OP_NE(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        if left_type == right_type:
            return 'RW_BOOL'
        else:
            raise Exception("Type error: both operands must be of the same type")



    def visit_RW_IF(self, node):
        condition_type = self.visit(node.value)
        
        print(f"Condition type: {condition_type}")

        if condition_type == 'RW_BOOL':
            self.enter_scope()
            self.visit(node.children[1])
            self.exit_scope()

            if len(node.children) > 2:
                self.enter_scope()
                self.visit(node.children[2])
                self.exit_scope()
        else:
            raise Exception("Type error: condition in 'if' statement must be boolean")



parser = Parser("""
    int n = 5;
    int resultado = 1;
    while (n > 1){
        resultado = n * resultado;
        n = n - 1;
    }
    print(resultado);
""")

tree = parser.parse()
tree.print_tree()
semantics = Semantics()
semantics.visit(tree)
print("No semantic errors found")
