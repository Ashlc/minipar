from _parser import Parser
from enum_tokens import TokenEnums as en
from lexer import Lexer
from syntax_tree import SyntaxNode


class Semantics:
    def __init__(self):
        self.global_env = {}
        self.local_envs = [{}]

    def enter_scope(self):

        self.local_envs.append({})

    def exit_scope(self):

        self.local_envs.pop()

    def update_global_variable(self, name, value, var_type):
        self.global_env[name] = {"type": var_type, "value": value}

    def get_operands(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        if not left.node_type == en.RW_INT or not right.node_type == en.RW_INT:
            raise Exception("Type error: both operands must be integers")
        return {"left": left.value, "right": right.value}

    def visit(self, node):
        method_name = f"visit_{node.node_type.name}"
        print(f"Visiting {node.node_type.name}")
        if method_name.replace("visit_", "") in (
            "OP_GT",
            "OP_LT",
            "OP_GTE",
            "OP_LTE",
            "OP_EQ",
            "OP_NEQ",
        ):
            method_name = "visit_comparison"
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
        value = self.visit(node.children[0]).value
        if value is None:
            raise Exception("ValueError: cannot print None")

    def visit_OP_ASSIGN(self, node):
        name = node.children[0].value
        value_node = node.children[1]

        if (
            value_node.node_type is not en.NUM
            and value_node.node_type is not en.STRING_LITERAL
        ):
            value_node = self.visit(value_node)

        value = value_node.value
        var_type = value_node.node_type

        if name in self.global_env:
            self.update_global_variable(name, value, var_type)
        else:
            self.local_envs[-1][name] = {"type": var_type, "value": value}

    def visit_ID(self, node):
        name = node.value

        for env in reversed(self.local_envs):
            if name in env:
                found_var = env[name]
                print(f"Found value: {found_var}")
                if isinstance(found_var["value"], int):
                    return SyntaxNode(en.RW_INT, found_var["value"])
                elif isinstance(found_var["value"], str):
                    return SyntaxNode(en.STRING_LITERAL, found_var["value"])
                else:
                    return SyntaxNode(env[name]["type"], env[name]["value"])

        if name in self.global_env:
            return SyntaxNode(
                self.global_env[name]["type"], self.global_env[name]["value"]
            )

        raise Exception(f"NameError: name '{name}' is not defined")

    def visit_NUM(self, node):
        if isinstance(node.value, int):
            return SyntaxNode(en.RW_INT, node.value)
        raise Exception("Type error: expected integer")

    def visit_STRING_LITERAL(self, node):
        if isinstance(node.value, str):
            return SyntaxNode(en.STRING_LITERAL, node.value)
        else:
            raise Exception("Type error: expected string")

    def visit_BLOCK(self, node):

        prev_global_env = self.global_env.copy()

        self.enter_scope()
        for statement_node in node.children:
            self.visit(statement_node)
        self.exit_scope()

        for name, value in self.global_env.items():
            if name not in prev_global_env or prev_global_env[name] != value:
                self.update_global_variable(name, value)

    def visit_OP_MULTIPLY(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] * op["right"])

    def visit_OP_DIVIDE(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] / op["right"])

    def visit_OP_PLUS(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] + op["right"])

    def visit_OP_MINUS(self, node):
        op = self.get_operands(node)
        return SyntaxNode(en.NUM, op["left"] - op["right"])

    def visit_RW_PAR(self, node):
        self.enter_scope()
        self.visit(node.children[0])
        self.exit_scope()

    def visit_RW_SEQ(self, node):
        self.enter_scope()
        for child in node.children:
            self.visit(child)
        self.exit_scope()

    def visit_RW_FOR(self, node):
        self.enter_scope()
        print(f"[FOR] Node: {node.print_tree()}")
        condition_node = self.visit(node.value)
        init = self.visit(node.children[0])
        increment = self.visit(node.children[1])
        block_node = self.visit(node.children[2])

        print(f"Condition node: {condition_node}")
        print(f"Init: {init}")
        print(f"Increment: {increment}")

        if not condition_node == en.RW_BOOL:
            raise Exception("Type error: condition must be boolean")

        if not init.node_type == en.RW_INT or not increment.node_type == en.RW_INT:
            raise Exception("Type error: both operands must be integers")

        if not block_node.node_type == en.RW_INT:
            raise Exception("Type error: block must return an integer")

        self.exit_scope()

    def visit_RW_WHILE(self, node):
        condition_node = node.value
        block_node = node.children[0]

        condition_value = self.visit(condition_node).value

        if condition_value:  # If condition is true, analyze the block
            self.enter_scope()  # Enter scope for the block analysis
            self.visit(block_node)  # Analyze the block
            self.exit_scope()  # Exit the block scope

    def visit_comparison(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])

        if left.node_type == right.node_type:
            return en.RW_BOOL

        else:
            raise Exception("Type error: both operands must be of the same type")

    def visit_RW_IF(self, node):
        condition_type = self.visit(node.value)
        node.print_tree()

        if condition_type == en.RW_BOOL:
            self.enter_scope()
            self.visit(node.children[0])
            self.exit_scope()

        else:
            raise Exception("Type error: condition in 'if' statement must be boolean")


parser = Parser(
    """
    int n = 5;
    int resultado = 1;
    n = n + 1;
    if (n > 5) {
        resultado = resultado * n;
    }
    while (n > 0) {
        resultado = resultado * n;
        n = n - 1;
    }
    par {
        print(resultado);
    }
    
    seq {
        int i = 0;
        for (i = 0; i < 5; i = i + 1) {
            print(i);
        }
    }
    
    for (int i = 0; i < 5; i = i + 1) {
        print(i);
    }
"""
)

tree = parser.parse()
tree.print_tree()
semantics = Semantics()
semantics.visit(tree)
print("No semantic errors found")
