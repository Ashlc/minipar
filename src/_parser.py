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
                print(f"[parse_program] Adding assignment node to program: {assignment_node}")
                syntax_tree.add_children(assignment_node)
            elif self.current_token[0] == en.RW_INT:
                declaration_node = self.parse_declaration()
                print(f"[parse_program] Adding declaration node to program: {declaration_node}")
                syntax_tree.add_children(declaration_node)  # Add declaration node to the program
            elif self.current_token[0] in (en.RW_IF, en.RW_WHILE, en.RW_FOR, en.RW_PRINT, en.RW_INPUT):
                statement_node = self.parse_statement()
                print(f"[parse_program] Adding statement node to program: {statement_node}")
                syntax_tree.add_children(statement_node)
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token[0]}")
        return syntax_tree
    
    def parse_declaration(self):
        token = self.current_token
        self.eat(en.RW_INT)
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        
        # Create a new node for the assignment
        assignment_node = SyntaxNode(en.OP_ASSIGN)
        
        print(f"identifier: {identifier}")
        
        # Create a new node for the identifier
        identifier_node = SyntaxNode(en.ID, identifier)
        
        # Add the identifier and value nodes as children of the assignment node
        assignment_node.add_children(identifier_node)
        assignment_node.add_children(value)
        
        # Create a new node for the declaration
        declaration_node = SyntaxNode(en.RW_INT)
        declaration_node.add_children(assignment_node)
        
        return declaration_node
    
    def parse_block(self):
        block_node = SyntaxNode(en.BLOCK)
        self.eat(en.DL_LBRACE)
        while self.current_token[0] != en.DL_RBRACE:
            statement_node = self.parse_statement()
            block_node.add_children(statement_node)
        self.eat(en.DL_RBRACE)
        return block_node


    
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
        else_block = None
        if self.current_token[0] == en.RW_ELSE:
            self.eat(en.RW_ELSE)
            else_block = self.parse_block()
        if_node = SyntaxNode(en.RW_IF, condition)
        if_node.add_children(if_block)
        if else_block:
            if_node.add_children(else_block)
        return if_node

        
    def parse_while_statement(self):
        self.eat(en.RW_WHILE)
        self.eat(en.DL_LPAREN)
        condition = self.parse_expression()
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        
        # Create a SyntaxNode for WHILE loop with condition and block as children
        while_node = SyntaxNode(en.RW_WHILE)
        while_node.add_children(condition)
        while_node.add_children(block)

        print("[parse_while_statement] Returning node with type: (WHILE)")
        return while_node
    
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
        channel_node = SyntaxNode(en.RW_C_CHANNEL)
        channel_node.add_children(block)
        return channel_node
    
    def parse_seq(self):
        self.eat(en.RW_SEQ)
        self.eat(en.DL_LPAREN)
        
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_seq] Returning node with type: (SEQ)")
        seq_node = SyntaxNode(en.RW_SEQ)
        seq_node.add_children(block)
        return seq_node
    
    def parse_par(self):
        self.eat(en.RW_PAR)
        self.eat(en.DL_LPAREN)
        
        self.eat(en.DL_RPAREN)
        block = self.parse_block()
        print("[parse_par] Returning node with type: (PAR)")
        par_node = SyntaxNode(en.RW_PAR)
        par_node.add_children(block)
        return par_node
    
    def parse_print(self):
        self.eat(en.RW_PRINT)
        self.eat(en.DL_LPAREN)
        expression = self.parse_expression()
        self.eat(en.DL_RPAREN)
        self.eat(en.DL_SEMICOLON)  
        print_node = SyntaxNode(en.RW_PRINT)
        print_node.add_children(expression)
        return print_node
    
    def parse_declaration(self):
        token = self.current_token
        self.eat(en.RW_INT)
        identifier = self.current_token
        self.eat(en.ID)
        self.eat(en.OP_ASSIGN)
        value = self.parse_expression()
        self.eat(en.DL_SEMICOLON)
        
        # Create a new node for the assignment
        assignment_node = SyntaxNode(en.OP_ASSIGN)
        
        # Create a new node for the identifier
        identifier_node = SyntaxNode(en.ID, identifier[1])
        
        # Add the identifier and value nodes as children of the assignment node
        identifier_node.add_children(value)
        assignment_node.add_children(identifier_node)
        
        # Create a new node for the declaration and add the assignment node as its child
        declaration_node = SyntaxNode(en.RW_INT)
        declaration_node.add_children(assignment_node)

        return declaration_node
    
    def parse_assignment(self):
        identifier = self.current_token
        self.eat(en.ID)
        token = self.current_token
        if token[0] == en.OP_ASSIGN:
            self.eat(en.OP_ASSIGN)
            value = self.parse_expression()
            self.eat(en.DL_SEMICOLON)
            print(f"[parse_assignment] Returning node with type: ({en.OP_ASSIGN})")
            assignment_node = SyntaxNode(en.OP_ASSIGN)
            identifier_node = SyntaxNode(en.ID, identifier[1])
            assignment_node.add_children(identifier_node)
            assignment_node.add_children(value)
            return assignment_node
        elif token[0] in (en.OP_PLUS, en.OP_MINUS, en.OP_MULTIPLY, en.OP_DIVIDE):
            operator = token[0]
            self.eat(operator)
            value = self.parse_expression()
            self.eat(en.DL_SEMICOLON)
            operation_node = SyntaxNode(operator)
            operation_node.add_children(SyntaxNode(en.ID, identifier[1]))
            operation_node.add_children(value)
            print(f"[parse_assignment] Returning node with type: ({operator})")
            return operation_node
        
        else:
            raise SyntaxError("Invalid assignment statement")

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token[0] in (en.OP_PLUS, en.OP_MINUS, en.OP_MULTIPLY, en.OP_DIVIDE, en.OP_GT, en.OP_LT, en.OP_GE, en.OP_LE, en.OP_EQ, en.OP_NE):
            token = self.current_token
            self.eat(token[0])
            operator_node = SyntaxNode(token[0])  # Create a new node for the operator
            operator_node.add_children(node)  # Add the left-hand side (LHS) of the operation
            operator_node.add_children(self.parse_term())  # Add the right-hand side (RHS) of the operation
            node = operator_node
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
                return SyntaxNode(en.RW_INT, token[1])
            elif token[0] == en.DL_LPAREN:
                self.eat(en.DL_LPAREN)
                node = self.parse_expression()
                self.eat(en.DL_RPAREN)
                return node
            elif token[0] == en.ID:
                identifier_token = self.current_token
                self.eat(en.ID)
                return SyntaxNode(en.ID, identifier_token[1])
            elif token[0] == en.NUM:
                num_token = self.current_token
                self.eat(en.NUM)
                return SyntaxNode(en.NUM, num_token[1])
            elif token[0] == en.STRING_LITERAL:
                string_token = self.current_token
                self.eat(en.STRING_LITERAL)
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
# syntax_tree.print_tree()