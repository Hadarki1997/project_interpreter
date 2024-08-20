from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    lexer = Lexer(code)
    tokens = lexer.lex()
    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter()
    results = []

    if isinstance(tree, list):
        for statement in tree:
            result = interpreter.visit(statement)
            if result is not None:
                results.append(result)
    else:
        result = interpreter.visit(tree)
        if result is not None:
            results.append(result)

    for result in results:
        print(result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        input_filename = sys.argv[1]
        if not input_filename.endswith('.lambda'):
            print("Error: File must have a .lambda extension")
        else:
            run_file(input_filename)
    else:
        print("Usage: python file_runner.py <program.lambda>")