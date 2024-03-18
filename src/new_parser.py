from enum_tokens import TokenEnums as en
from lexer import Lexer
from syntax_tree import SyntaxNode

class Parser:
    def __init__(self, file):
        self.lexer = Lexer(file)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        print("[PARSER] Begin...")
        syntax_tree = self.parse_program()
        print("[PARSER] Complete.")
        return syntax_tree

    def parse_program(self):
        syntax_tree = SyntaxNode(en.PROGRAM)
        while self.current_token[0] != en.EOF:
            if self.current_token[0] == en.ID:
                assignment_node = self.parse_assignment()
                syntax_tree.add_children(assignment_node)
            elif self.current_token[0] == en.RW_INT:
                declaration_node = self.parse_declaration()
                syntax_tree.add_children(declaration_node)
            # Add more cases for other statements as needed
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        return syntax_tree

    # Other parsing methods

    def parse_declaration(self):
        token = self.current_token
        self.eat(en.RW_INT)
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        
        # Create a new node for the declaration and add it to the syntax tree
        declaration_node = SyntaxNode(en.DECLARATION, [identifier, value])
        print("[parse_declaration] Returning node with type: (DECLARATION)")
        return declaration_node

    def parse_assignment(self):
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        
        # Create a new node for the assignment and add it to the syntax tree
        assignment_node = SyntaxNode(en.OP_ASSIGN, [identifier, value])
        print("[parse_assignment] Returning node with type: (ASSIGNMENT)")
        return assignment_node
    def parse_expression(self):
        node = self.parse_term()

        while self.current_token[0] in (en.OP_PLUS, en.OP_MINUS, en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ):
            token = self.current_token
            self.eat(token[0])
            node = SyntaxNode(token[0], [node, self.parse_term()])

        print(f"[parse_expression] Returning node with type: ({node.node_type})")
        return node

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token[0] in (en.OP_MULTIPLY, en.OP_DIVIDE):
            token = self.current_token
            self.eat(token[0])
            node = SyntaxNode(token[0], [node, self.parse_factor()])

        return node

    def parse_factor(self):
        token = self.current_token

        if token[0] == en.RW_INT:
            self.eat(en.RW_INT)
            print(f"[parse_factor] Parsed factor: {token[1]}, creating new node with type: {token[0]}")
            return SyntaxNode(token[0])

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
            return SyntaxNode(en.ID, identifier_token[1])

        elif token[0] == en.NUM:
            num_token = self.current_token
            self.eat(en.NUM)
            print(f"[parse_factor] Parsed factor: {num_token[1]}, creating new node with type: {num_token[0]}")
            return SyntaxNode(en.NUM, num_token[1])

        elif token[0] == en.STRING_LITERAL:
            string_token = self.current_token
            self.eat(en.STRING_LITERAL)
            print(f"[parse_factor] Parsed factor: {string_token[1]}, creating new node with type: {string_token[0]}")
            return SyntaxNode(en.STRING_LITERAL, string_token[1])

        else:
            raise SyntaxError(f"Invalid factor: {token[0]}, expected an identifier, integer, or expression")

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        elif self.current_token[0] == en.EOF:
            raise SyntaxError(f"Unexpected end of file: expected {token_type}")
        else:
            raise SyntaxError(f"Unexpected token: expected {token_type}, got {self.current_token[0]}")

# Instantiate and use the parser
parser = Parser("your_input_file.txt")
syntax_tree = parser.parse()
syntax_tree.print_tree()  # Print the syntax tree for debugging or visualization
