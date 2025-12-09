# test_functions.py
from pyparser.main import parse_python
import pytest


class TestFunctionDefinition:

    def test_function_def_simple(self):
        """
        Tests a basic function definition with a simple string return statement
        by asserting the entire expected AST dictionary.
        """
        code = "def foo():\n    return 'bar'"

        expected_ast = {
            "type": "Module",
            "body": [
                {
                    "type": "FunctionDef",
                    "name": "foo",
                    "args": {"args": [], "vararg": None, "kwarg": None, "defaults": []},
                    "body": [
                        {
                            "type": "Return",
                            "value": {
                                "type": "Constant",
                                "value": "bar",
                                "dtype": "STRING",
                            },
                        }
                    ],
                    "decorator_list": [],
                    "returns": None,
                    "async": False,
                }
            ],
        }

        result = parse_python(code)
        assert result == expected_ast

    def test_function_with_args_and_binary_op(self):
        """
        Tests a function with arguments and a return value that is a binary operation (x + y).
        """
        code = "def add(x, y):\n    return x + y"
        expected_ast = {
            "body": [
                {
                    "args": {
                        "args": [],
                        "defaults": [
                            {"annotation": None, "name": "x"},
                            {"annotation": None, "name": "y"},
                        ],
                        "kwarg": None,
                        "vararg": None,
                    },
                    "async": False,
                    "body": [
                        {
                            "type": "Return",
                            "value": {
                                "left": {"ctx": "Load", "id": "x", "type": "Name"},
                                "operator": "+",
                                "right": {"ctx": "Load", "id": "y", "type": "Name"},
                                "type": "BinaryOp",
                            },
                        }
                    ],
                    "decorator_list": [],
                    "name": "add",
                    "returns": None,
                    "type": "FunctionDef",
                }
            ],
            "type": "Module",
        }

        result = parse_python(code)
        assert result == expected_ast

    def test_return_function_call(self):
        """
        Tests a function that returns the result of another function call with arguments.
        """
        code = "def caller():\n    return target(1, 2)"

        expected_ast = {
            "type": "Module",
            "body": [
                {
                    "type": "FunctionDef",
                    "name": "caller",
                    "args": {"args": [], "vararg": None, "kwarg": None, "defaults": []},
                    "body": [
                        {
                            "type": "Return",
                            "value": {
                                "type": "Call",
                                "identifier": {
                                    "type": "Name",
                                    "id": "target",
                                    "ctx": "Load",
                                },
                                "args": [
                                    {
                                        "type": "Constant",
                                        "value": "1",
                                        "dtype": "NUMBER",
                                    },
                                    {
                                        "type": "Constant",
                                        "value": "2",
                                        "dtype": "NUMBER",
                                    },
                                ],
                            },
                        }
                    ],
                    "decorator_list": [],
                    "returns": None,
                    "async": False,
                }
            ],
        }

        result = parse_python(code)
        assert result == expected_ast
