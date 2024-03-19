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
        if method_name.replace('visit_', '') in ('OP_GT', 'OP_LT', 'OP_GTE', 'OP_LTE', 'OP_EQ', 'OP_NEQ'):
            method_name = 'visit_comparison'
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
        self.current_type = en.RW_INT
        self.visit_children(node)

    def visit_RW_BOOL(self, node):
        self.current_type = en.RW_BOOL
        self.visit_children(node)

    def visit_RW_STRING(self, node):
        self.current_type = en.RW_STRING
        self.visit_children(node)

    def visit_RW_C_CHANNEL(self, node):
        self.current_type = en.RW_C_CHANNEL
        self.visit_children(node)
        
    def visit_RW_PRINT(self, node):
        value = self.visit(node.children[0])
        print(f"Printing: {value}")

    def visit_OP_ASSIGN(self, node):
        print("[OP_ASSIGN NODE TREE]")
        node.print_tree()
        name = node.children[0].value  # Get the name from the identifier node
        value = node.children[1].value
        
        # if node.children:
        #     name = node.children[0].value  # Get the name from the identifier node
        #     print(f"[OP_ASSIGN] Variable name: {name}")
        #     print(f"[OP_ASSIGN] Checking node children")
        #     print(node.children)
        #     id_node = self.visit(node.children[0])
        #     print("[OP_ASSIGN] IDENTIFIER TREE")
        #     id_node.print_tree()
            
        #     if id_node is not None:
        #         print(f"Value: {id_node.children[1].value}")
        #         value = self.visit(node.children[1])

        if name in self.types[-1] and self.types[-1][name] != self.current_type:
            raise Exception(f"Type error: variable '{name}' was declared as {self.types[-1][name]} but assigned a value of type {self.current_type}")

        print(f"Assigning {value} to {name}")
        
        self.environments[-1][name] = value
        self.types[-1][name] = self.current_type

    def visit_ID(self, node):
        node.print_tree()
        name = node.value  # Get the name from the ID node
        for env in reversed(self.environments):
            if name in env:
                print(f"Found {name} in environment, returning value: {env[name]}")
                return env[name]
        raise Exception(f"NameError: name '{name}' is not defined")

    def visit_NUM(self, node):
        return en.RW_INT

    def visit_STRING_LITERAL(self, node):
        return en.RW_INT
    
    def visit_BLOCK(self, node):
        self.enter_scope()
        for statement_node in node.children:
            self.visit(statement_node)
        self.exit_scope()

    def visit_OP_PLUS(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        if not left == en.RW_INT or not right== en.RW_INT:
            raise Exception("Type error: both operands must be integers")
        return en.RW_INT
    
    def visit_RW_WHILE(self, node):
        node.print_tree()
        condition_node = node.children[0]
        block_node = node.children[1]

        while self.visit(condition_node):
            self.visit(block_node)

    def visit_OP_MINUS(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        if not left == en.RW_INT or not right== en.RW_INT:
            raise Exception("Type error: both operands must be integers")
        return en.RW_INT

    def visit_comparison(self, node):
        node.print_tree()
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])
        
        print(f"Left type: {left_type}")
        print(f"Right type: {right_type}")
                    
        if isinstance(left_type, int):
            left_type = en.RW_INT
            
        if isinstance(right_type, int):
            right_type = en.RW_INT
                                
        if left_type == right_type:
            return en.RW_BOOL
        
        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_RW_IF(self, node):
        condition_type = self.visit(node.value)
        print(f"Condition type: {condition_type}")

        if condition_type == en.RW_BOOL:
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
