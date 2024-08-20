from interpreter import Interpreter
from lexer import Lexer
from parser import Parser


def repl():
    interpreter = Interpreter()
    while True:
        try:
            text = input('calc> ')
            lexer = Lexer(text)
            tokens = lexer.lex()
            parser = Parser(tokens)
            tree = parser.parse()
            result = interpreter.visit(tree)
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    repl()
