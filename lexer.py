
# Token Types
INTEGER, BOOLEAN, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, \
AND, OR, NOT, EQ, NEQ, GT, LT, GEQ, LEQ, \
ID, COMMA, IF, DEFUN, LAMBDA, DOT, EOF, ELSE = (
    'INTEGER', 'BOOLEAN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
    'AND', 'OR', 'NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
    'ID', 'COMMA', 'IF', 'DEFUN', 'LAMBDA', 'DOT', 'EOF', 'ELSE'
)

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1  # מספר שורה נוכחי
        self.column = 1  # מספר עמודה נוכחי
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                self.advance()  # לדלג על תו ה-newline בסוף ההערה

    def lex(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char.isdigit():
                tokens.append(Token(INTEGER, self.integer()))
            elif self.current_char == '+':
                tokens.append(Token(PLUS, '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS, '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL, '*'))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV, '/'))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(MOD, '%'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN, ')'))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token('LBRACE', '{'))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token('RBRACE', '}'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(COMMA, ','))
                self.advance()
            elif self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                tokens.append(Token(AND, '&&'))
            elif self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                tokens.append(Token(OR, '||'))
            elif self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(EQ, '=='))
            elif self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token(NEQ, '!='))
                else:
                    tokens.append(Token(NOT, '!'))
                    self.advance()
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(GEQ, '>='))
                    self.advance()
                else:
                    tokens.append(Token(GT, '>'))
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(LEQ, '<='))
                    self.advance()
                else:
                    tokens.append(Token(LT, '<'))
            elif self.current_char.isalpha():
                tokens.append(self.id())
            else:
                raise ValueError(f"Unknown token: {repr(self.current_char)} at line {self.line}, column {self.column}")
        tokens.append(Token(EOF))
        return tokens
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        if result == 'True':
            return Token(BOOLEAN, True)
        elif result == 'False':
            return Token(BOOLEAN, False)
        elif result == 'if':
            return Token(IF, result)
        elif result == 'defun':
            return Token(DEFUN, result)
        elif result == 'lambd':
            return Token(LAMBDA, result)
        elif result == 'else':
            return Token(ELSE, result)
        elif result.lower() == 'not':  # Ensure 'not' keyword is recognized
            return Token(NOT, result)
        else:
            return Token(ID, result)