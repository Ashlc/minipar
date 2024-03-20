# Entry point for the PyC interpreter

import sys
import os
import argparse
from interpreter import Interpreter
import threading
import socket

input_file = """

string server = "localhost";
string procedure = "calculadora";
string type = "client";
c_channel(procedure, server, type);

"""

interpreter = Interpreter(input_file, export=True)
output = interpreter.run()
interpreter.save_tree()
