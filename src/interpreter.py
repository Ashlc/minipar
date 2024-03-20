from semantic import SemanticAnalyzer
from _parser import Parser
from enum_tokens import TokenEnums as en
import json
import threading
import socket

# from server import Server
# from client import Client


def c_channel(host, type):
    this_addr = (host, 5546)
    size = 1024
    format = "utf-8"
    procedure = None

    if type == "server":
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(this_addr)
        server.listen()
        print("[SERVER] Waiting for connections...")
        first = True

        while True:
            conn, addr = server.accept()

            if first:
                print(f"[SERVER] Connected to {addr}")
                conn.send("What procedure do you wish to execute?".encode(format))
                first = False

            a = conn.recv(size).decode(format)

            if a == "exit":
                break

            if a == "calculadora":
                procedure = a
                conn.send("Awaiting expression...".encode("ascii"))
                continue

            if procedure == "calculadora":
                result = calculate(a)
                print(f"[SERVER] Sending result: {result} to {addr}")
                conn.send(str(result).encode("ascii"))
            else:
                conn.send("Invalid command".encode("ascii"))

    elif type == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(this_addr)
        client.send(procedure.encode(format))


def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"


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
