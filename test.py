import unittest

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class BaseTestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def run_test_case(self, text, expected):
        lexer = Lexer(text)
        tokens = lexer.lex()
        parser = Parser(tokens)
        tree = parser.parse()
        result = self.interpreter.visit(tree)
        self.assertEqual(result, expected)


class TestArithmeticOperations(BaseTestInterpreter):

    def test_addition(self):
        self.run_test_case("3 + 5", 8)

    def test_negative_addition(self):
        self.run_test_case("-3 + -5", -8)

    def test_subtraction(self):
        self.run_test_case("10 - 4", 6)

    def test_multiplication(self):
        self.run_test_case("6 * 7", 42)

    def test_multiplication_fraction(self):
        self.run_test_case("16 * (9/8)", 16)

    def test_division(self):
        self.run_test_case("8 / 2", 4)

    def test_modulus(self):
        self.run_test_case("10 % 3", 1)


class TestBooleanOperations(BaseTestInterpreter):

    def test_and(self):
        self.run_test_case("True && False", False)

    def test_or(self):
        self.run_test_case("True || False", True)

    def test_not(self):
        self.run_test_case("!True", False)

    def test_equal(self):
        self.run_test_case("True == True", True)

    def test_not_equal(self):
        self.run_test_case("True != False", True)

    def test_greater_than(self):
        self.run_test_case("5 > 3", True)

    def test_less_than(self):
        self.run_test_case("5 < 3", False)

    def test_greater_than_or_equal(self):
        self.run_test_case("5 >= 5", True)

    def test_less_than_or_equal(self):
        self.run_test_case("5 <= 3", False)


class TestConditionalStatements(BaseTestInterpreter):

    def test_if_true(self):
        self.run_test_case("if True 1 else 2", 1)

    def test_if_false(self):
        self.run_test_case("if False 1 else 2", 2)

    def test_if_greater_than(self):
        self.run_test_case("if 5 > 3 10 else 20", 10)

    def test_if_less_than(self):
        self.run_test_case("if 3 > 5 10 else 20", 20)


class TestFunctionDefinitionsAndCalls(BaseTestInterpreter):

    def test_call_add_function(self):
        self.run_test_case("defun add(a, b) { a + b }", None)
        self.run_test_case("add(2, 3)", 5)

    def test_call_multiply_function(self):
        self.run_test_case("defun multiply(x, y) { x * y }", None)
        self.run_test_case("multiply(4, 5)", 20)

    def test_recursive_function(self):
        self.run_test_case("defun factorial(n) { n ==0 || n * factorial(n - 1) }", None)
        self.run_test_case("factorial(4)", 24)

    def test_call_sum_function(self):
        self.run_test_case("defun sum(a, b, c) { a + b + c }", None)
        self.run_test_case("sum(1, 2, 3)", 6)

    def test_nested_single_function(self):
        self.run_test_case("defun single(x) { x }", None)
        self.run_test_case("single(single(5))", 5)


class TestLambdaExpressions(BaseTestInterpreter):

    def test_lambda_add(self):
        self.run_test_case("lambd(a, b) ( a + b )(6, 7)", 13)

    def test_lambda_square(self):
        self.run_test_case("lambd(x) ( x * x )(5)", 25)


class TestDivisionByZero(BaseTestInterpreter):

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.run_test_case("5 / 0", "Division by zero")

    def test_division_by_zero_in_expression(self):
        with self.assertRaises(ZeroDivisionError):
            self.run_test_case("10 / (2 - 2)", "Division by zero")


class TestBooleanLogicAndFunctions(BaseTestInterpreter):

    def setUp(self):
        super().setUp()
        self.run_test_case("defun iseven(x) { x % 2 == 0 }", None)
        self.run_test_case("defun isodd(x) { x % 2 != 0 }", None)

    def test_call_iseven_function(self):
        self.run_test_case("iseven(4)", True)

    def test_call_isodd_on_even(self):
        self.run_test_case("isodd(4)", False)

    def test_call_isodd_on_odd(self):
        self.run_test_case("isodd(5)", True)


if __name__ == '__main__':
    unittest.main()
