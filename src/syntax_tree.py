from enum_tokens import TokenEnums as en
import json
import threading
import socket

class SyntaxNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.scope = None
        self.nparams = None
        self.children = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def set_scope(self, scope):
        self.scope = scope

    def set_nparams(self, nparams):
        self.nparams = nparams

    def print_tree(self, level=0):
        indent = "    " * level
        print(
            f'{indent}{self.node_type} of value {self.value if self.value is not None else "--"}'
        )

        for child in self.children:
            child.print_tree(level + 1)

    def to_json(self):
        def convert_enum_to_str(value):
            if isinstance(value, en):
                return value.name
            return value

        node_json = {
            "node_type": convert_enum_to_str(self.node_type),
            "value": (
                self.value.to_json()
                if isinstance(self.value, SyntaxNode)
                else convert_enum_to_str(self.value) if self.value is not None else "--"
            ),
            "children": [child.to_json() for child in self.children],
        }
        return node_json

    def evaluate(self, indent_level=0):
        indent = "    " * indent_level
        if self.node_type == en.PROGRAM:
            code = ""
            for child in self.children:
                code += child.evaluate(indent_level) + "\n"
            return code
        if self.node_type == en.RW_INT:
            output = ""
            for child in self.children:
                output += child.evaluate(indent_level) + "\n"
            return output

        # Adicionei um {indent} aqui pq no while quando ele ia mudar o valor do i ele não tinha indentação
        elif self.node_type == en.OP_ASSIGN:
            variable = self.children[0].value
            expression = self.children[1]
            return f"{indent}{variable} = {expression.evaluate()}"

        elif self.node_type == en.OP_PLUS:

            left = self.children[0].evaluate()
            right = self.children[1].evaluate()
            return f"({left} + {right})"

        elif self.node_type == en.ID:
            return self.value

        elif self.node_type == en.NUM:
            return str(self.value)

        elif self.node_type == en.STRING_LITERAL:
            return f'"{self.value}"'

        # Eu acho que o problema no for é que a sintaxe que tu ta criando não existe em python
        # Então eu acho que a alternativa mais viável seria fazer um loop while mas usando as 
        # informações dadas. Seria tipo:
        #   init = self.children[0].evaluate(indent_level + 1)
        #   condition = self.value.evaluate()
        #   increment = self.children[1].evaluate(indent_level + 1)
        #   block = self.children[2].evaluate(indent_level + 1)
        #   return f"{indent}init\nwhile {condition}:\n{increment}\n{block}"

        # Eu fiz e funciona se ele estiver sozinho, mas não se vc fizer nested.
        elif self.node_type == en.RW_FOR:
            init = self.children[0].evaluate()
            condition = self.value.evaluate()
            increment = self.children[1].evaluate(indent_level + 1)
            block = self.children[2].evaluate()
            return f"{indent}{init}\nwhile {condition}:\n{increment}\n{block}"
            #return f"{indent}for {init}; {condition}; {increment}:\n{block}"


        # Antes o IF era OBRIGADO a ter um else, eu mudei pra funcionar mesmo sem.
        elif self.node_type == en.RW_IF:
            condition = self.value.evaluate()
            block_true = self.children[0].evaluate(indent_level + 1)
            if len(self.children) > 1:
                block_false = self.children[1].evaluate(indent_level + 1)
                return f"{indent}if {condition}:\n{block_true}{indent}else:\n{block_false}"
            else:
                return f"{indent}if {condition}:\n{block_true}"
            

        # Eu tirei o {indent} daqui pq no while a primeira linha tinha o dobro de identação. E não afetou as outras funções (eu acho)
        elif self.node_type == en.BLOCK:
            block_code = ""
            for child in self.children:
                block_code += child.evaluate(indent_level + 1) + "\n"
            return f"{block_code}"

        elif self.node_type == en.RW_PRINT:
            expression = self.children[0].evaluate()
            return f"{indent}print({expression})\n"

        elif self.node_type in [
            en.OP_GT,
            en.OP_LT,
            en.OP_GE,
            en.OP_LE,
            en.OP_EQ,
            en.OP_NE,
        ]:
            left = self.children[0].evaluate()
            right = self.children[1].evaluate()
            if self.node_type == en.OP_GT:
                return f"{left} > {right}"
            elif self.node_type == en.OP_LT:
                return f"{left} < {right}"
            elif self.node_type == en.OP_GE:
                return f"{left} >= {right}"
            elif self.node_type == en.OP_LE:
                return f"{left} <= {right}"
            elif self.node_type == en.OP_EQ:
                return f"{left} == {right}"
            elif self.node_type == en.OP_NE:
                return f"{left} != {right}"

        # While feito e funcionando, mesmo quando usado nested.
        elif self.node_type == en.RW_WHILE:
            condition = self.value.evaluate()
            block = self.children[0].evaluate(indent_level + 1)
            return f"{indent}while {condition}:\n{block}"
        
        elif self.node_type == en.RW_PAR:
            # Eu não faço a menor ideia de como a gente separaria uma thread da outra, 
            # então não sei como implementar, mas a ideia seria algo como feito a seguir
            blocks = []
            # Pega os N blocos
            block = self.children[0].evaluate(indent_level - 1)
            blocks.append(block)
            print(block)
            return f"par_block({blocks})"
        
        # Funciona.
        elif self.node_type == en.RW_SEQ:
            block = self.children[0].evaluate(indent_level - 1)
            return f"{indent}{block}"
        
        # Eu não sei como ficou a sintaxe do channel, mas ACHO que é assim
        # Além disso, OP_INCREMENT e OP_DECREMENT não existem na gramática, mas nós temos OP_INC e OP_DEC, não ajeitei isso mas é resolver no parser.
        # Also c_channel ta com problema no parser, não sei o pq. Talvez seja eu escrevendo na sintaxe errada mesmo.
        
        elif self.node_type == en.C_CHANNEL:
            operation = self.children[0].evaluate(indent_level)
            comp1 = self.children[1].evaluate(indent_level)
            comp2 = self.children[2].evaluate(indent_level)
            return f"{indent}c_channel({operation}, {comp1}, {comp2})\n"

        # Eu não sei se era pra ter uma função calculadora_send e calculadora_receive,
        # Então n sei como faza pra implementar elas
        # Mas se tiver é só fazer como ai em cima e estruturar a chamada da função.
        # As funçoes no main eu já fiz.
        else:
            raise ValueError(f"Invalid node_type enum {self.node_type}")
