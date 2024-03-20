from semantic import SemanticAnalyzer
from _parser import Parser
from enum_tokens import TokenEnums as en
import json
import threading
import socket
from server import Server
from client import Client


def c_channel(procedure, server, type):
    print(f"Connecting to {server} with procedure {procedure}")
    server = Server(server)
    server.set_procedure(procedure)
    print(f"Server running on {server.addr}")


def par_block(block):
    thread = threading.Thread(target=lambda: exec(block[0]))
    thread.start()


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
        self.tree.print_tree()
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
