# Entry point for the PyC interpreter

import sys
import os
import argparse
from interpreter import Interpreter
import threading
import socket

input_file = """

c_channel("localhost", "server")

"""

interpreter = Interpreter(input_file, export=True)
output = interpreter.run()
interpreter.save_tree()
