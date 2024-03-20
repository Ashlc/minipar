from interpreter import Interpreter

type = input("Caminho do arquivo fonte: ")
with open(type, 'r') as file:
    # Lê os conteúdos do arquivo
    contents = file.read()


input_file = contents

# Roda o interpretador e salva a árvore
interpreter = Interpreter(input_file, export=True)
output = interpreter.run()
interpreter.save_tree()
