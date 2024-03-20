from semantic import SemanticAnalyzer
from _parser import Parser
from enum_tokens import TokenEnums as en
import json


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
