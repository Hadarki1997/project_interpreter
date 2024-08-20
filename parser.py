# Token Types
INTEGER, BOOLEAN, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, \
AND, OR, NOT, EQ, NEQ, GT, LT, GEQ, LEQ, \
ID, COMMA, IF, DEFUN, LAMBDA, DOT, EOF, ELSE = (
    'INTEGER', 'BOOLEAN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
    'AND', 'OR', 'NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
    'ID', 'COMMA', 'IF', 'DEFUN', 'LAMBDA', 'DOT', 'EOF', 'ELSE'
)
from lexer import Token
class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.name = token.value

class Function(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Lambda(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class Call(AST):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class If(AST):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token(EOF)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return Token(EOF)

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.advance()
            return Num(token)
        elif token.type == BOOLEAN:
            self.advance()
            return Bool(token)
        elif token.type == ID:
            return self.function_call_or_var()
        elif token.type == LPAREN:
            self.advance()
            expr = self.expression()
            if self.current_token.type == RPAREN:
                self.advance()
                return expr
            else:
                raise ValueError("Expected ')'")
        elif token.type == MINUS:
            self.advance()
            return UnaryOp(token, self.factor())
        elif token.type == NOT:
            self.advance()
            return UnaryOp(token, self.factor())
        else:
            raise ValueError(f"Unexpected token: {token.type}")

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            self.advance()
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expression(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS, AND, OR, EQ, NEQ, GT, LT, GEQ, LEQ):
            token = self.current_token
            self.advance()
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def if_statement(self):
        self.advance()  # skip 'if'
        condition = self.expression()
        then_branch = self.expression()
        else_branch = None
        if self.current_token.type == ELSE:
            self.advance()
            else_branch = self.expression()
        return If(condition, then_branch, else_branch)

    def function_definition(self):
        self.advance()  # skip 'defun'
        func_name = self.current_token.value
        self.advance()  # skip function name
        self.advance()  # skip '('
        params = []
        while self.current_token.type != RPAREN:
            params.append(self.current_token.value)
            self.advance()
            if self.current_token.type == COMMA:
                self.advance()
        self.advance()  # skip ')'
        if self.current_token.type == 'LBRACE':
            self.advance()  # skip '{'
            body = self.parse_block()
            if self.current_token.type != 'RBRACE':
                raise ValueError("Expected '}'")
            self.advance()  # skip '}'
        else:
            body = [self.expression()]  # Wrap single expression in a list
        return Function(func_name, params, body)


    def lambda_expression(self):
        self.advance()  # skip 'lambd'
        self.advance()  # skip '('
        params = []
        while self.current_token.type != RPAREN:
            params.append(self.current_token.value)
            self.advance()
            if self.current_token.type == COMMA:
                self.advance()
        self.advance()  # skip ')'
        body = self.expression()

        lambda_node = Lambda(params, body)

        if self.current_token.type == LPAREN:
            self.advance()  # Skip '('
            args = []
            while self.current_token.type != RPAREN:
                args.append(self.expression())
                if self.current_token.type == COMMA:
                    self.advance()
            self.advance()  # Skip ')'
            return Call(lambda_node, args)

        return lambda_node

    def parse_block(self):
        statements = []
        while self.current_token.type not in ('RBRACE', EOF):
            statements.append(self.expression())
            if self.current_token.type == COMMA:
                self.advance()  # Skip comma and continue
        return statements

    def parse(self):
        statements = []
        while self.current_token.type != EOF:
            if self.current_token.type == IF:
                statements.append(self.if_statement())
            elif self.current_token.type == DEFUN:
                func_def = self.function_definition()
                statements.append(func_def)
            elif self.current_token.type == LAMBDA:
                statements.append(self.lambda_expression())
            else:
                statements.append(self.expression())

            if self.current_token.type == COMMA:
                self.advance()  # Skip comma between statements

        return statements

    def function_call_or_var(self):
        token = self.current_token
        self.advance()
        if self.current_token.type == LPAREN:
            self.advance()  # consume '('
            args = []
            if self.current_token.type != RPAREN:
                args.append(self.expression())
                while self.current_token.type == COMMA:
                    self.advance()
                    args.append(self.expression())
            if self.current_token.type != RPAREN:
                raise ValueError("Expected ')'")
            self.advance()  # consume ')'
            return Call(Var(token), args)
        else:
            return Var(token)