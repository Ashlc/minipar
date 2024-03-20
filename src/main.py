# Entry point for the PyC interpreter

import sys
import os
import argparse
from interpreter import Interpreter

input_file = """
int a = 10; # Comment
if (a > 5) {
  print("Hello");
} else {
  print("World");
}
"""

interpreter = Interpreter(input_file, export=True)
output = interpreter.run()
interpreter.save_tree()
