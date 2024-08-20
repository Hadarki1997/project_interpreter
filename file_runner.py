from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

# Function to run a file containing the source code
def run_file(file_path):
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        code = file.read()

    # Initialize the Lexer with the code and generate tokens
    lexer = Lexer(code)
    tokens = lexer.lex()

    # Pass the tokens to the Parser and generate the AST
    parser = Parser(tokens)
    tree = parser.parse()

    # Initialize the Interpreter to execute the AST
    interpreter = Interpreter()
    results = []

    # If the AST is a list (multiple statements), visit each statement
    if isinstance(tree, list):
        for statement in tree:
            result = interpreter.visit(statement)
            if result is not None:
                results.append(result)
    else:
        # Otherwise, just visit the single statement/tree
        result = interpreter.visit(tree)
        if result is not None:
            results.append(result)

    # Print the results of the execution
    for result in results:
        print(result)

# Main entry point for running the script
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        input_filename = sys.argv[1]
        # Ensure the file has the correct extension
        if not input_filename.endswith('.lambda'):
            print("Error: File must have a .lambda extension")
        else:
            # Run the file if the extension is correct
            run_file(input_filename)
    else:
        # Print usage information if the wrong number of arguments is provided
        print("Usage: python file_runner.py <program.lambda>")
