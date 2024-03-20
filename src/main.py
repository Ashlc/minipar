# Entry point for the PyC interpreter

import sys
import os
import argparse
from interpreter import Interpreter
import threading
import socket

type = input("Caminho do arquivo fonte: ")
with open(type, 'r') as file:
    # Read the contents of the file
    contents = file.read()

# Now 'contents' holds the entire contents of the file
input_file = contents

interpreter = Interpreter(input_file, export=True)
output = interpreter.run()
interpreter.save_tree()
