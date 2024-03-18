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
            elif self.current_token[0] == en.RW_INT:
                declaration_node = self.parse_declaration()
                syntax_tree.add_children(declaration_node)
            elif self.current_token[0] in (en.RW_IF, en.RW_WHILE, en.RW_FOR, en.RW_PRINT, en.RW_INPUT):
                statement_node = self.parse_statement()
                syntax_tree.add_children(statement_node)
            else:
                # Handle other cases or raise an error if needed
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        return syntax_tree

    
    def parse_declaration(self):
        print("Parsing a declaration...")
        token = self.current_token
        self.eat(en.DECLARATION)  # Consume 'declaration' token
        identifier = self.current_token
        self.eat(en.ID)  # Consume identifier token
        self.eat(en.DL_LPAREN)  # Consume '('
        # Parse parameters, if any (not implemented here)
        self.eat(en.DL_RPAREN)  # Consume ')'
        # Parse function body (not implemented here)
        print(f"Parsed declaration: {identifier[1]}")
        self.eat(en.DL_SEMICOLON)  # Consume ';'
        print("[parse_declaration] Returning node with type: (DECLARATION)")
        return SyntaxNode(en.DECLARATION, [identifier])
    
    def parse_block(self):
        print("Parsing a block...")
        block_node = SyntaxNode("BLOCK")
        self.eat(en.DL_LBRACE)  # Consume '{'
        while self.current_token[0] != en.DL_RBRACE:
            # Parse statements inside the block
            statement_node = self.parse_statement()
            block_node.add_children(statement_node)
        self.eat(en.DL_RBRACE)  # Consume '}'
        print("[parse_block] Returning node with type: (BLOCK)")
        return block_node
    
    def parse_statement(self):
        # Parse a complete statement
        token_type = self.current_token[0]

        if token_type == en.RW_INT:
            return self.parse_declaration()
        elif token_type == en.ID:
            return self.parse_assignment()
        elif token_type == en.RW_IF:
            return self.parse_if_statement()
        elif token_type == en.RW_WHILE:
            return self.parse_while_statement()
        elif token_type == en.RW_FOR:
            return self.parse_for_statement()
        elif token_type == en.RW_PRINT:
            return self.parse_print()
        elif token_type == en.RW_INPUT:
            return self.parse_input()
        else:
            # Handle other types of statements or expressions
            return self.parse_expression()

        
    def parse_if_statement(self):
        print("Parsing an if statement...")
        self.eat(en.RW_IF)  # Consume 'if' token
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        if_block = self.parse_block()
        if self.current_token[0] == en.RW_ELSE:
            self.eat(en.RW_ELSE)
            else_block = self.parse_block()
            print("[parse_if_statement] Returning node with type: (IF)")
            return SyntaxNode(en.RW_IF.name, [condition, if_block, else_block])
        else:
            print("[parse_if_statement] Returning node with type: (IF)")
            return SyntaxNode(en.RW_IF.name, [condition, if_block])

        
    def parse_while_statement(self):
        print("Parsing a while statement...")
        self.eat(en.RW_WHILE)
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        print(f"Condition parsed: {condition}")
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        # Do not consume semicolon here
        print("[parse_while_statement] Returning node with type: (WHILE)")
        return SyntaxNode(en.RW_WHILE.name, [condition, block])

    
    def parse_for_statement(self):
        print("Parsing a for statement...")
        self.eat(en.RW_FOR)
        self.eat(en.DL_LPAREN)
        init = self.parse_assignment()
        condition = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        increment = self.parse_assignment()
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_for_statement] Returning node with type: (FOR)")
        return SyntaxNode(en.RW_FOR.name, [init, condition, increment, block])
    
    def parse_c_channel(self):
        print("Parsing a c channel...")
        self.eat(en.RW_C_CHANNEL)
        self.eat(en.DL_LPAREN)
        # Parse channel parameters (not implemented here)
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_c_channel] Returning node with type: (C_CHANNEL)")
        return SyntaxNode(en.RW_C_CHANNEL.name, [block])
    
    def parse_seq(self):
        print("Parsing a seq...")
        self.eat(en.RW_SEQ)
        self.eat(en.DL_LPAREN)
        # Parse seq parameters (not implemented here)
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_seq] Returning node with type: (SEQ)")
        return SyntaxNode(en.RW_SEQ.name, [block])
    
    def parse_par(self):
        print("Parsing a par...")
        self.eat(en.RW_PAR)
        self.eat(en.DL_LPAREN)
        # Parse par parameters (not implemented here)
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_par] Returning node with type: (PAR)")
        return SyntaxNode(en.RW_PAR.name, [block])
    
    def parse_function_call(self):
        print("Parsing a function call...")
        self.eat(en.CALL)  # Consume 'call' token
        identifier = self.current_token
        self.eat(en.ID)  # Consume identifier token
        self.eat(en.DL_LPAREN)  # Consume '('
        # Parse arguments, if any (not implemented here)
        self.eat(en.DL_RPAREN)  # Consume ')'
        print(f"Parsed function call: {identifier[1]}")
        print("[parse_function_call] Returning node with type: (CALL)")
        return SyntaxNode(en.CALL, [identifier])
    
    def parse_print(self):
        print("Parsing a print statement...")
        self.eat(en.RW_PRINT)
        self.eat(en.DL_LPAREN)
        expression = self.parse_expression()
        self.eat(en.DL_RPAREN)
        self.eat(en.DL_SEMICOLON)  # Consume the semicolon to mark the end of the statement
        print("[parse_print] Returning node with type: (PRINT)")
        return SyntaxNode(en.RW_PRINT.name, [expression])

    
    def parse_declaration(self):
        print("Parsing a declaration...")
        token = self.current_token
        self.eat(en.RW_INT)
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        print(f"Parsed declaration: {identifier[1]} = {value.node_type}")
        self.eat(en.DL_SEMICOLON)
        print(f"[parse_declaration] Returning node with type: ({en.RW_INT})")
        return SyntaxNode(en.RW_INT, [identifier, value])
    
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
            self.eat(token[0])
            node = SyntaxNode(token[0].name, [node, self.parse_term()])

        while self.current_token[0] in (en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ):
            token = self.current_token
            print(f"[parse_expression] Found a comparison operator: {token[0]}")
            self.eat(token[0])
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
            
        elif token[0] == en.STRING_LITERAL:
            string_token = self.current_token
            self.eat(en.STRING_LITERAL)
            print(f"[parse_factor] Parsed factor: {string_token[1]}, creating new node with type: {string_token[0]}")
            return SyntaxNode(en.STRING_LITERAL.name, string_token[1])  # Create syntax node with string value

        else:
            raise SyntaxError(f"Invalid factor: {token[0]}, expected an identifier, integer, or expression")


    def eat(self, token_type):
        print(f"Eating token: {token_type}")
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
            print(f"New current token: {self.current_token[0]} of value {self.current_token[1]}")
        elif self.current_token[0] == en.EOF:
            raise SyntaxError(f"Unexpected end of file: expected {token_type}")
        else:
            raise SyntaxError(f"Unexpected token: expected {token_type}, got {self.current_token[0]}")


# Test the parser

parser = Parser("""
int x = 5;
int y = 6;
int z = x + y;

print("Hello, World!");

if (x > y) {
    print("x is greater than y");
} else {
    print("y is greater than x");
}

while (x > 0) {
    print(x);
    x = x - 1;
}
""")

tree = parser.parse()
print("Printing syntax tree...")
tree.print_tree()

