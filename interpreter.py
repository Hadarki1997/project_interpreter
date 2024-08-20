# Token Types
INTEGER, BOOLEAN, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, \
    AND, OR, NOT, EQ, NEQ, GT, LT, GEQ, LEQ, \
    ID, COMMA, IF, DEFUN, LAMBDA, DOT, EOF, ELSE = (
    'INTEGER', 'BOOLEAN', 'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'LPAREN', 'RPAREN',
    'AND', 'OR', 'NOT', 'EQ', 'NEQ', 'GT', 'LT', 'GEQ', 'LEQ',
    'ID', 'COMMA', 'IF', 'DEFUN', 'LAMBDA', 'DOT', 'EOF', 'ELSE'
)

from parser import Var, Function

# Interpreter class that executes the parsed Abstract Syntax Tree (AST)
class Interpreter:
    def __init__(self):
        self.global_scope = {}  # Global scope for storing variables and functions
        self.output = []        # Output list to store the results of execution

    # Main visit method that dispatches to the appropriate visit method
    def visit(self, node):
        if isinstance(node, list):
            return self.visit_statements(node)  # Handle a list of statements
        method_name = f'visit_{type(node).__name__.lower()}'  # Dynamically find the correct visit method
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    # Visit a list of statements and execute them in sequence
    def visit_statements(self, statements):
        result = None
        for statement in statements:
            result = self.visit(statement)
            if result is not None:
                self.output.append(result)  # Collect non-None results
        return result

    # Generic visit method that raises an error if no specific visit method is found
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    # Visit a number node and return its value
    def visit_num(self, node):
        return node.value

    # Visit a boolean node and return its value
    def visit_bool(self, node):
        return node.value

    # Visit a variable node and retrieve its value from the global scope
    def visit_var(self, node):
        if node.name in self.global_scope:
            return self.global_scope[node.name]
        else:
            raise NameError(f"Undefined variable: {node.name}")

    # Visit a binary operation node and execute the operation
    def visit_binop(self, node):
        left = self.visit(node.left)  # Evaluate the left operand

        # Short-circuit evaluation for AND and OR logical operators
        if node.op.type == OR:
            if left:
                return left  # Return early if OR condition is true
            return self.visit(node.right)
        elif node.op.type == AND:
            if not left:
                return left  # Return early if AND condition is false
            return self.visit(node.right)

        right = self.visit(node.right)  # Evaluate the right operand

        # Perform the actual binary operation
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

    # Visit a unary operation node and execute the operation
    def visit_unaryop(self, node):
        expr = self.visit(node.expr)  # Evaluate the operand
        if node.op.type == MINUS:
            return -expr  # Negation
        elif node.op.type == NOT:
            return not expr  # Logical NOT

    # Visit a function definition node and store it in the global scope
    def visit_function(self, node):
        self.global_scope[node.name] = node  # Store the function by its name

    # Visit a lambda function node and return a callable function object
    def visit_lambda(self, node):
        def lambda_func(*args):
            if len(args) != len(node.params):
                raise TypeError("Argument count mismatch")
            local_scope = dict(zip(node.params, args))  # Map parameters to arguments
            previous_scope = self.global_scope.copy()  # Save current scope
            self.global_scope.update(local_scope)  # Update scope with lambda arguments
            result = self.visit(node.body)  # Execute lambda body
            self.global_scope = previous_scope  # Restore previous scope
            return result

        return lambda_func

    # Visit a function call node and execute the function
    def visit_call(self, node):
        func = self.visit(node.func)  # Evaluate the function to call
        args = [self.visit(arg) for arg in node.args]  # Evaluate arguments

        # Handle function calls defined in the code
        if isinstance(node.func, Var) and node.func.name in self.global_scope:
            func_node = self.global_scope[node.func.name]
            if isinstance(func_node, Function):
                previous_scope = self.global_scope.copy()  # Save current scope
                local_scope = dict(zip(func_node.params, args))  # Map parameters to arguments
                self.global_scope.update(local_scope)  # Update scope with function arguments
                result = self.visit(func_node.body)  # Execute function body
                self.global_scope = previous_scope  # Restore previous scope
                return result
            else:
                raise TypeError(f"{node.func.name} is not callable")
        elif callable(func):
            return func(*args)  # Handle lambda functions or built-in callables
        else:
            raise NameError(f"Undefined function: {node.func.name}")

    # Visit an if statement node and execute the appropriate branch
    def visit_if(self, node):
        condition = self.visit(node.condition)  # Evaluate the condition
        if condition:
            return self.visit(node.then_branch)  # Execute then branch
        elif node.else_branch is not None:
            return self.visit(node.else_branch)  # Execute else branch if present
        return None
