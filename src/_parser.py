from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from lexer import Lexer

class Parser:
    
    def __init__(self, file):
        self.lexer = Lexer(file)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        return self.parse_expression()
    
    def parse_block(self):
        self.eat(en.DL_LBRACE)
        statements = []

        while self.current_token[0] != en.DL_RBRACE:
            statements.append(self.parse_statement())
            self.eat(en.DL_SEMICOLON)  # Expecting semicolon after each statement

        self.eat(en.DL_RBRACE)
        return SyntaxNode(en.BLOCK, statements)

    def parse_statement(self):
        if self.current_token[0] == en.DL_LBRACE:
            return self.parse_block()
        elif self.current_token[0] == en.ID:
            return self.parse_assignment()
        else:
            raise SyntaxError("Invalid statement")

    def parse_assignment(self):
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_EQ)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        return SyntaxNode(en.OP_ASSIGN, [identifier, value])

    def parse_expression(self):
        node = self.parse_term()

        while self.current_token[0] in (en.OP_PLUS, en.OP_MINUS):
            token = self.current_token
            self.eat([token[0]])
            node = SyntaxNode(token, [node, self.parse_term()])

        return node
    

    def parse_term(self):
        node = self.parse_factor()

        while self.current_token[0] in (en.OP_MULTIPLY, en.OP_DIVIDE):
            token = self.current_token
            self.eat([token[0]])
            node = SyntaxNode(token, [node, self.parse_factor()])

        return node

    def parse_factor(self):
        token = self.current_token

        if [token[0]] == en.RW_INT:
            self.eat(en.RW_INT)
            return SyntaxNode(token)

        elif [token[0]] == en.DL_LPAREN:
            self.eat(en.DL_LPAREN)
            node = self.parse_expression()
            self.eat(en.DL_RPAREN)
            return node

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError("Unexpected token")

# Test the parser

parser = Parser("""
int a = 10;
int b = 20;
int c = a + b;
""")

tree = parser.parse()
tree.print_tree()