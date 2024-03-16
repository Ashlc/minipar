from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from lexer import Lexer

class Parser:
    
    def __init__(self, file):
        self.lexer = Lexer(file)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        print("Beginning parsing...")
        syntax_tree = self.parse_program()
        print("Parsing complete.")
        return syntax_tree

    def parse_program(self):
        syntax_tree = SyntaxNode("PROGRAM")
        while self.current_token[0] != en.EOF:
            if self.current_token[0] == en.ID:
                assignment_node = self.parse_assignment()
                
                syntax_tree.add_children(assignment_node)
            else:
                expression_node = self.parse_expression()
                syntax_tree.add_children(expression_node)
        return syntax_tree
    
    def parse_assignment(self):
        print("Parsing an assignment...")
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        print(f"Parsed assignment: {identifier[1]} = {value.node_type}")
        self.eat(en.DL_SEMICOLON)
        print(f"[parse_assignment] Returning node with type: ({en.OP_ASSIGN})")
        return SyntaxNode(en.OP_ASSIGN, [identifier, value])

    def parse_expression(self):
        print("Parsing an expression...")
        node = self.parse_term()

        while self.current_token[0] in (en.OP_PLUS, en.OP_MINUS):
            token = self.current_token
            print(f"[parse_expression] Found an operator: {token[0]}")
            self.eat(token[0])  # Change from self.eat([token[0]]) to self.eat(token[0])
            node = SyntaxNode(token[0].name, [node, self.parse_term()])

        print(f"[parse_expression] Returning node with type: ({node.node_type})")
        return node

    
    def parse_term(self):
        print("Parsing a term...")
        node = self.parse_factor()

        while self.current_token[0] in (en.OP_MULTIPLY, en.OP_DIVIDE):
            token = self.current_token
            self.eat([token[0]])
            node = SyntaxNode(token[0].name, [node, self.parse_factor()])

        print(f"[parse_term] Returning node with type: ({node.node_type})")
        return node

    def parse_factor(self):
        print("Parsing a factor...")
        token = self.current_token

        if token[0] == en.RW_INT:
            self.eat(en.RW_INT)
            print(f"[parse_factor] Parsed factor: {token[1]}, creating new node with type: {token[0]}")
            return SyntaxNode(token[0].name)

        elif token[0] == en.DL_LPAREN:
            self.eat(en.DL_LPAREN)
            node = self.parse_expression()
            self.eat(en.DL_RPAREN)
            print(f"[parse_factor] Returning node with type: ({node.node_type})")
            return node

        elif token[0] == en.ID:
            identifier_token = self.current_token
            self.eat(en.ID)
            print(f"[parse_factor] Parsed factor: {token[1]}, creating new node with type: {token[0]}")
            return SyntaxNode(en.ID.name, identifier_token[1])  # Create syntax node with identifier name

        elif token[0] == en.NUM:
            num_token = self.current_token
            self.eat(en.NUM)
            print(f"[parse_factor] Parsed factor: {num_token[1]}, creating new node with type: {num_token[0]}")
            return SyntaxNode(en.NUM.name, num_token[1])  # Create syntax node with number value

        else:
            raise SyntaxError(f"Invalid factor: {token[0]}, expected an identifier, integer or expression")

    def eat(self, token_type):
        print(f"Eating token: {token_type}")
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
            print(f"New current token: {self.current_token[0]} of value {self.current_token[1]}")
        else:
            raise SyntaxError(f"Unexpected token: expected {token_type}, got {self.current_token[0]}")

# Test the parser

parser = Parser("""
int a = 10;
int b = 20;
int c = a + b;
""")

tree = parser.parse()
print("Printing syntax tree...")
tree.print_tree()

