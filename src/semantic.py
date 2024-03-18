from _parser import Parser
from enum_tokens import TokenEnums as en
from lexer import Lexer

class Semantics:
    def __init__(self):
        self.environments = [{}]  # A list of dictionaries. Each dictionary represents a scope.
        self.types = [{}]

    def enter_scope(self):
        self.environments.append({})
        self.types.append({})

    def exit_scope(self):
        self.environments.pop()
        self.types.pop()

    def visit(self, node):
        method_name = f'visit_{str(node.node_type).replace("TokenEnums.", "")}'
        print(method_name)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{node.node_type} method defined")

    # Visit methods for each node type
    def visit_PROGRAM(self, node):
        for child in node.children:
            self.visit(child)

    def visit_RW_INT(self, node):
        self.current_type = 'RW_INT'
        self.visit_TokenEnums_OP_ASSIGN(node)
    
    def visit_RW_BOOL(self, node):
        self.current_type = 'RW_BOOL'
    
    def visit_RW_STRING(self, node):
        self.current_type = 'RW_STRING'

    def visit_RW_C_CHANNEL(self, node):
        self.current_type = 'RW_C_CHANNEL'       

    def visit_TokenEnums_OP_ASSIGN(self, node):
        name = node.value[0][1]
        value_node = node.value[1]
        value = self.visit(value_node)

        print(f"Assigning {value} to {name}")

        if name in self.types[-1] and self.types[-1][name] != self.current_type:
            raise Exception(f"Type error: variable '{name}' was declared as {self.types[-1][name]} but assigned a value of type {self.current_type}")
        self.environments[-1][name] = value
        self.types[-1][name] = self.current_type

    def visit_ID(self, node):
        name = node.value
        for env in reversed(self.environments):
            if name in env:
                return env[name]
        raise Exception(f"NameError: name '{name}' is not defined")
    
    def visit_NUM(self, node):
        return 'RW_INT'
    
    def visit_STRING_LITERAL(self, node):
        return 'RW_STRING'
    
    def visit_OP_PLUS(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        return "RW_INT"

    def visit_OP_MINUS(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        return "RW_INT"

    def visit_OP_MULTIPLY(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        return "RW_INT"

    def visit_OP_DIVIDE(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == "RW_INT" or not right== "RW_INT":
            raise Exception("Type error: both operands must be integers")
        if right == 0:
            raise Exception("Math error: division by zero")
        return "RW_INT"

    def visit_OP_EQ(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if left != right:
            raise Exception("Type error: both operands must be of the same type")
        return 'RW_BOOL'
    
    def visit_OP_NOT_EQ(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if left != right:
            raise Exception("Type error: both operands must be of the same type")
        return 'RW_BOOL'

    def visit_OP_LT(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if left != right:
            raise Exception("Type error: both operands must be of the same type")
        return 'RW_BOOL'

    def visit_OP_GT(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if left != right:
            raise Exception("Type error: both operands must be of the same type")
        return 'RW_BOOL'
    
    def visit_OP_AND(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == 'RW_BOOL' or not right == 'RW_BOOL':
            raise Exception("Type error: both operands must be booleans")
        return 'RW_BOOL'

    def visit_OP_NOT(self, node):
        if len(node.children) == 0:
            value = self.visit(node.value[0])
        else:
            value = self.visit(node.children[0])
        if not value == 'RW_BOOL':
            raise Exception("Type error: operand must be a boolean")
        return 'RW_BOOL'

    def visit_OP_OR(self, node):
        if len(node.children) == 0:
            left = self.visit(node.value[0])
            right = self.visit(node.value[1])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
        if not left == 'RW_BOOL' or not right == 'RW_BOOL':
            raise Exception("Type error: both operands must be booleans")
        return 'RW_BOOL'

    def visit_RW_IF(self, node):
        if len(node.children) == 0:
            expected_input = node.value[1]
            condition = self.visit(node.value[0])
        else:
            expected_input = node.value[1]
            condition = self.visit(node.children[0])
        print(condition)
        if condition == 'RW_BOOL':
            self.enter_scope() # Enter a new scope for the 'then' branch
            self.visit(expected_input)  # Visit the 'then' branch
            self.exit_scope() # Exit the scope for the 'then' branch

            if len(node.children) > 2:
                self.enter_scope() # Enter a new scope for the 'else' branch
                self.visit(node.children[2])  # Visit the 'else' branch, if it exists
                self.exit_scope() # Exit the scope for the 'then' branch                
        else:
            raise Exception("Type error: condition in 'if' statement must be boolean")

    def visit_RW_FOR(self, node):
        # Assuming the 'for' node has three children: initialization, condition, and increment
        if len(node.children) == 0:
            init_node = self.visit(node.value[0])
            cond_node = self.visit(node.value[1])
            inc_node = self.visit(node.value[2])
        else:
            init_node = self.visit(node.children[0])
            cond_node = self.visit(node.children[1])
            inc_node = self.visit(node.children[2])

        # Enter a new scope for the loop
        self.enter_scope()

        # Visit the initialization node
        self.visit(init_node)

        # Check the condition
        while True:
            cond_value = self.visit(cond_node)
            if cond_value != 'RW_BOOL':
                raise Exception(f"Type error: condition in 'for' statement must be boolean, got {cond_value}")
            if not cond_value:
                break

            # Visit the body of the loop
            for child in node.body:
                self.visit(child)

            # Visit the increment node
            self.visit(inc_node)

        # Exit the loop's scope
        self.exit_scope()
    
    def visit_RW_WHILE(self, node):
        # Assuming the 'while' node has two children: condition and body
        if len(node.children) == 0:
            cond_node = self.visit(node.value[0])
            body_node = self.visit(node.value[1])
        else:
            cond_node = self.visit(node.children[0])
            body_node = self.visit(node.children[1])

        # Enter a new scope for the loop
        self.enter_scope()

        # Check the condition
        while True:
            cond_value = self.visit(cond_node)
            if cond_value != 'RW_BOOL':
                raise Exception(f"Type error: condition in 'while' statement must be boolean, got {cond_value}")
            if not cond_value:
                break

            # Visit the body of the loop
            self.visit(body_node)

        # Exit the loop's scope
        self.exit_scope()
    
    def visit_RW_SEQ(self, node):
        if len(node.children) == 0:
            body_node = self.visit(node.value[0])
        else:
            body_node = self.visit(node.children[0])
        return body_node
    
    def visit_RW_PAR(self, node):
        if len(node.children) == 0:
            body_node = self.visit(node.value[0])
        else:
            body_node = self.visit(node.children[0])
        return body_node
    
    def visit_BLOCK(self, node):
        pass

# Dividing is getting a sintax error
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
semantics = Semantics()
semantics.visit(tree)  # This will raise an exception if there are any semantic errors
print("No semantic errors found")  # If no exceptions were raised, the program is semantically correct