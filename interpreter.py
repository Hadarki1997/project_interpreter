# Token Types
INTEGER, BOOLEAN, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, \
    AND, OR, NOT, EQ, NEQ, GT, LT, GEQ, LEQ, \
    ID, COMMA, IF, DEFUN, LAMBDA, DOT, EOF, ELSE = (
    'INTEGER', 'BOOLEAN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
    'AND', 'OR', 'NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
    'ID', 'COMMA', 'IF', 'DEFUN', 'LAMBDA', 'DOT', 'EOF', 'ELSE'
)
from parser import Var, Function


class Interpreter:
    def __init__(self):
        self.global_scope = {}
        self.output = []

    def visit(self, node):
        if isinstance(node, list):
            return self.visit_statements(node)
        method_name = f'visit_{type(node).__name__.lower()}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def visit_statements(self, statements):
        result = None
        for statement in statements:
            result = self.visit(statement)
            if result is not None:
                self.output.append(result)
        return result

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_num(self, node):
        return node.value

    def visit_bool(self, node):
        return node.value

    def visit_var(self, node):
        if node.name in self.global_scope:
            return self.global_scope[node.name]
        else:
            raise NameError(f"Undefined variable: {node.name}")

    def visit_binop(self, node):
        left = self.visit(node.left)

        # Short-circuit evaluation for AND and OR
        if node.op.type == OR:
            if left:
                return left
            return self.visit(node.right)
        elif node.op.type == AND:
            if not left:
                return left
            return self.visit(node.right)

        right = self.visit(node.right)

        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == DIV:
            return left // right
        elif node.op.type == MOD:
            return left % right
        elif node.op.type == EQ:
            return left == right
        elif node.op.type == NEQ:
            return left != right
        elif node.op.type == GT:
            return left > right
        elif node.op.type == LT:
            return left < right
        elif node.op.type == GEQ:
            return left >= right
        elif node.op.type == LEQ:
            return left <= right

    def visit_unaryop(self, node):
        expr = self.visit(node.expr)
        if node.op.type == MINUS:
            return -expr
        elif node.op.type == NOT:
            return not expr

    def visit_function(self, node):
        # Store the function definition in the global scope
        self.global_scope[node.name] = node

    def visit_lambda(self, node):
        def lambda_func(*args):
            if len(args) != len(node.params):
                raise TypeError("Argument count mismatch")
            local_scope = dict(zip(node.params, args))
            previous_scope = self.global_scope.copy()
            self.global_scope.update(local_scope)
            result = self.visit(node.body)
            self.global_scope = previous_scope
            return result

        return lambda_func

    def visit_call(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]

        if isinstance(node.func, Var) and node.func.name in self.global_scope:
            func_node = self.global_scope[node.func.name]
            if isinstance(func_node, Function):
                # Create a new scope for the function call
                previous_scope = self.global_scope.copy()
                local_scope = dict(zip(func_node.params, args))
                self.global_scope.update(local_scope)

                # Execute the function body
                result = self.visit(func_node.body)

                # Restore the previous scope
                self.global_scope = previous_scope
                return result
            else:
                raise TypeError(f"{node.func.name} is not callable")
        elif callable(func):
            return func(*args)
        else:
            raise NameError(f"Undefined function: {node.func.name}")

    def visit_if(self, node):
        condition = self.visit(node.condition)
        if condition:
            return self.visit(node.then_branch)
        elif node.else_branch is not None:
            return self.visit(node.else_branch)
        return None
