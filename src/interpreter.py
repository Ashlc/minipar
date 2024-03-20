from semantic import SemanticAnalyzer
from _parser import Parser
from enum_tokens import TokenEnums as en
import json
import threading
import socket

# Eu declei o socket fora pra que as outras funções tenham acesso, não pensei em uma forma mais elegante de resolver esse problema.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def c_channel(operation, client_1, client_2):
    s.connect(({client_2}, 12345))
    message = f'User ID : {client_1} is asking for function {operation}'
    s.send(message.encode())

def calculadora_send(operação, valor1, valor2, resultado):
    message = f"{operação} {valor1} {valor2} {resultado}"
    s.send(message.encode())

# A descrição da atividade diz que o recieve tem que ser rodado pelo servidor. 
# Mas isso não faz nenhum sentido,já que é uma função que tem como parâmetros a parada que ele recebeu do cliente.
# Mas meio que quem recebe são as funçãões do socket.
# Fora que faz uma combinação do código em python pra rodar o servidor mais o código 
# em Minipar para rodar exclusivamente essa função é meio memes. 
# Então quem vai rodar é o user mesmo para receber o resultado.

# Assume que o recieve pracisa rodar em algum momento pro cliente fechar a conexão. 
def calculadora_receive(operação, valor1, valor2, resultado):
    data = s.recv(1024)
    message = data.decode()
    print(f'Mensagem recebida do servidor. O resultado da operação: {valor1} {operação} {valor2} é igual a: {message}')
    s.close()

def par_block(blocks):
    threads = []
    for block in blocks:
        thread = threading.Thread(target=lambda: exec(block))
        print(f"Thread {thread} started")
        thread.start()
        threads.append(thread)
        

    for thread in threads:
        thread.join()
        print(f"Thread {thread} finished")
 
    # Imagine que a gente tenha um código que separa as funções para cada thread e 
    # como resultado sejam armazenadas em uma lista:
    # blocks = [block1, block2, ...,blockn]
    # E definindo uma variável n para o número de threads
    # thread_code = ""
    # for block in blocks:
    #    thread = threading.Thread(target=lambda: exec(block))
    #    thread.start()
    #    thread.join()

# O SEQ não ironicamente não faz nada, então a função é só um pass mesmo.
def seq_block():
    pass


class Interpreter:

    def __init__(self, program, export=False):
        self.program = program
        self.semantic = SemanticAnalyzer()
        self.parser = Parser(program)
        self.output = []
        self.export = export
        self.tree = None

    def run(self):
        self.tree = self.parser.parse()
        if self.export:
            self.save_tree()
        self.semantic.visit(self.tree)
        exec(self.tree.evaluate())
        if self.export:
            self.save_tree()
        return self.output

    def save_tree(self):
        with open("tree.json", "w") as file:
            file.write(json.dumps(self.tree.to_json(), indent=4))
