from semantic import SemanticAnalyzer
from _parser import Parser
from enum_tokens import TokenEnums as en
import json
import threading
import socket

def _calculate(num1, operator, num2):

    result = 0
    if operator == '+':
        result =  float(num1) + float(num2)
    elif operator == '-':
        result = float(num1) - float(num2)
    elif operator == '*':
        result = float(num1) * float(num2)
    elif operator == '/':
        if num2 != 0:
            result = float(num1) / float(num2)
        else:
            return "Error: Invalid Operation, Division by zero!"
    else:
        return "Error: Invalid operator!"
    return result

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
        op = False
        conn, addr = server.accept()
        try:
            while True:
                print("Waiting for connections...")
                if first:
                    print(f"[SERVER] Connected to {addr}")
                    conn.send("What procedure do you wish to execute?".encode(format))
                    first = False

                a = conn.recv(size).decode(format)
                print(a)
                print(f"[SERVER] Received command: {a} from {addr}")
                if a == "exit":
                    print("Breaking")
                    break

                elif a == "calculadora" and op == False:
                    op = True
                    procedure = a
                    conn.send("Awaiting expression...".encode("ascii"))

                elif a.startswith("Expression:"):
                    print(f"[SERVER] Received expression: {a} from {addr}")
                    a = a.replace("Expression: ", "")
                    a = a.split()
                    print(a[0],a[1],a[2])
                    result = _calculate(a[0],a[1],a[2])
                    message = f"Result: {result}"
                    conn.send(message.encode("ascii"))
                    break
                else:
                    conn.send("Invalid command".encode("ascii"))
        finally:
            server.close()

    elif type == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(this_addr)
        message = client.recv(size).decode(format)
        print(f"Message from server: {message}")
        procedure = input("Enter the procedure you wish to execute: ")
        client.send(procedure.encode(format))
        while True:
            message = client.recv(size).decode(format)
            print(f"Message from server: {message}")

            if message == "Awaiting expression...":
                expression = input("Enter your expression: ")
                expression = "Expression: " + expression
                client.send(expression.encode(format))
                print(f"Sent expression: {expression}")
            elif "Invalid" in message:
                break
            elif message.startswith("Result"):
                print(f"Result: {message}")
                break
        client.close()

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
