from enum_tokens import TokenEnums

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def get_syntax_tree(self):
        return self.parser.parse()
    
    def interpret(self):
        syntax_tree = self.get_syntax_tree()
        self.traverse_tree(syntax_tree)
        
    def traverse_tree(self, node):
        if node.node_type == TokenEnums.OP_ASSIGN:
            self.handle_assignment(node)
        elif node.node_type == TokenEnums.DECLARATION:
            self.handle_function_declaration(node)
        elif node.node_type == TokenEnums.FUNCTION_CALL:
            self.handle_function_call(node)
        elif node.node_type == TokenEnums.PRINT:
            self.handle_print(node)
        elif node.node_type == TokenEnums.IF:
            self.handle_if(node)
        elif node.node_type == TokenEnums.WHILE:
            self.handle_while(node)
        
        for child in node.children:
            self.traverse_tree(child)