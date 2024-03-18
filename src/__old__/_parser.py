from syntax_tree import SyntaxNode
from enum_tokens import TokenEnums as en
from lexer import Lexer

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
            elif self.current_token[0] in (en.RW_IF, en.RW_WHILE, en.RW_FOR, en.RW_PRINT, en.RW_INPUT):
                statement_node = self.parse_statement()
                syntax_tree.add_children(statement_node)
            else:
                
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        return syntax_tree

    
    def parse_declaration(self):
        token = self.current_token
        self.eat(en.DECLARATION)  
        identifier = self.current_token
        self.eat(en.ID)  
        self.eat(en.DL_LPAREN)  
        
        self.eat(en.DL_RPAREN)  
        
        self.eat(en.DL_SEMICOLON)  
        print("[parse_declaration] Returning node with type: (DECLARATION)")
        return SyntaxNode(en.DECLARATION, [identifier])
    
    def parse_block(self):
        self.eat(en.DL_LBRACE)  
        while self.current_token[0] != en.DL_RBRACE:
            
            statement_node = self.parse_statement()
        self.eat(en.DL_RBRACE)  
        print("[parse_block] Returning node with type: (BLOCK)")
        return SyntaxNode(en.BLOCK, statement_node)

    
    def parse_statement(self):
        
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
            
            return self.parse_expression()

        
    def parse_if_statement(self):
        self.eat(en.RW_IF)  
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        if_block = self.parse_block()
        if self.current_token[0] == en.RW_ELSE:
            self.eat(en.RW_ELSE)
            else_block = self.parse_block()
            print("[parse_if_statement] Returning node with type: (IF)")
            return SyntaxNode(en.RW_IF, [condition, if_block, else_block])
        else:
            print("[parse_if_statement] Returning node with type: (IF)")
            return SyntaxNode(en.RW_IF, [condition, if_block])

        
    def parse_while_statement(self):
        self.eat(en.RW_WHILE)
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        
        print("[parse_while_statement] Returning node with type: (WHILE)")
        return SyntaxNode(en.RW_WHILE, [condition, block])

    
    def parse_for_statement(self):
        self.eat(en.RW_FOR)
        self.eat(en.DL_LPAREN)
        init = self.parse_assignment()
        condition = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        increment = self.parse_assignment()
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_for_statement] Returning node with type: (FOR)")
        return SyntaxNode(en.RW_FOR, [init, condition, increment, block])
    
    def parse_c_channel(self):
        self.eat(en.RW_C_CHANNEL)
        self.eat(en.DL_LPAREN)
        
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_c_channel] Returning node with type: (C_CHANNEL)")
        return SyntaxNode(en.RW_C_CHANNEL, [block])
    
    def parse_seq(self):
        self.eat(en.RW_SEQ)
        self.eat(en.DL_LPAREN)
        
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_seq] Returning node with type: (SEQ)")
        return SyntaxNode(en.RW_SEQ, [block])
    
    def parse_par(self):
        self.eat(en.RW_PAR)
        self.eat(en.DL_LPAREN)
        
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_par] Returning node with type: (PAR)")
        return SyntaxNode(en.RW_PAR, [block])
    
    def parse_function_call(self):
        self.eat(en.CALL)  
        identifier = self.current_token
        self.eat(en.ID)  
        self.eat(en.DL_LPAREN)  
        
        self.eat(en.DL_RPAREN)  
        print("[parse_function_call] Returning node with type: (CALL)")
        return SyntaxNode(en.CALL, identifier)
    
    def parse_print(self):
        self.eat(en.RW_PRINT)
        self.eat(en.DL_LPAREN)
        expression = self.parse_expression()
        self.eat(en.DL_RPAREN)
        self.eat(en.DL_SEMICOLON)  
        print("[parse_print] Returning node with type: (PRINT)")
        return SyntaxNode(en.RW_PRINT, expression)
    
    def parse_declaration(self):
        token = self.current_token
        self.eat(en.RW_INT)
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        
        # Create a new node for the assignment and add it to the syntax tree
        assignment_node = SyntaxNode(en.OP_ASSIGN, [identifier, value])
        print(f"[parse_declaration] Returning node with type: ({en.RW_INT})")
        return SyntaxNode(en.RW_INT, assignment_node)

    
    def parse_assignment(self):
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        print(f"[parse_assignment] Returning node with type: ({en.OP_ASSIGN})")
        return SyntaxNode(en.OP_ASSIGN, [identifier, value])

    def parse_expression(self):
        node = self.parse_term()

        while self.current_token[0] in (en.OP_PLUS, en.OP_MINUS):
            token = self.current_token
            self.eat(token[0])
            node = SyntaxNode(token[0], [node, self.parse_term()])

        while self.current_token[0] in (en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ):
            token = self.current_token
            self.eat(token[0])
            node = SyntaxNode(token[0], [node, self.parse_term()])

        print(f"[parse_expression] Returning node with type: ({node.node_type})")
        return node
    
    def parse_term(self):
        node = self.parse_factor()

        while self.current_token[0] in (en.OP_MULTIPLY, en.OP_DIVIDE):
            token = self.current_token
            self.eat([token[0]])
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



# Test

# parser = Parser(
#     """
#     int x = 30;
#     int y = 20;

#     if (x > y) {
#         print("x is greater than y");
#     } else {
#         print("y is greater than x");
#     }
# """
# )

# syntax_tree = parser.parse()

# print(syntax_tree.children)











