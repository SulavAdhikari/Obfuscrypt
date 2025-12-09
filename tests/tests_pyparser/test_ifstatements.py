from pyparser.main import parse_python
import pytest


class TestIfStatements:

    def test_simple_if(self):
        code = "if True :\n    x = 1"
        expected = {
            "type": "Module",
            "body": [
                {
                    "type": "IfStatement",
                    "test": {
                        "type": "Constant",
                        "value": True,
                        "dtype": "BOOLEAN"
                    },
                    "body": [
                        {
                            "type": "Assign",
                            "targets": [
                                {"type": "Name", "id": "x", "ctx": "Load"}
                            ],
                            "value": {
                                "type": "Constant",
                                "value": "1",
                                "dtype": "NUMBER"
                            },
                            "operator": "="
                        }
                    ],
                    "ifelse": None,
                    "else": None
                }
            ]
        }
        result = parse_python(code)
        assert result == expected

    def test_if_else(self):
        code = "if True:\n    x = 1\nelse:\n    x = 2"
        expected = {
            "type": "Module",
            "body": [
                {
                    "type": "IfStatement",
                    "test": {
                        "type": "Constant",
                        "value": True,
                        "dtype": "BOOLEAN"
                    },
                    "body": [
                        {
                            "type": "Assign",
                            "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                            "value": {"type": "Constant", "value": "1", "dtype": "NUMBER"},
                            "operator": "="
                        }
                    ],
                    "ifelse": None,
                    "else": {
                        "type": "ElseStatement",
                        "body": [
                            {
                                "type": "Assign",
                                "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                                "value": {"type": "Constant", "value": "2", "dtype": "NUMBER"},
                                "operator": "="
                            }
                        ],
                        "test": None
                    }
                }
            ]
        }
        result = parse_python(code)
        assert result == expected

    def test_if_elif_else(self):
        code = "if True:\n    x = 1\nelif False:\n    x = 2\nelse:\n    x = 3"
        expected = {
            "type": "Module",
            "body": [
                {
                    "type": "IfStatement",
                    "test": {
                        "type": "Constant",
                        "value": True,
                        "dtype": "BOOLEAN"
                    },
                    "body": [
                        {
                            "type": "Assign",
                            "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                            "value": {"type": "Constant", "value": "1", "dtype": "NUMBER"},
                            "operator": "="
                        }
                    ],
                    "ifelse": [
                        {
                            "type": "ElifStatement",
                            "test": {
                                "type": "Constant",
                                "value": False,
                                "dtype": "BOOLEAN"
                            },
                            "body": [
                                {
                                    "type": "Assign",
                                    "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                                    "value": {"type": "Constant", "value": "2", "dtype": "NUMBER"},
                                    "operator": "="
                                }
                            ]
                        }
                    ],
                    "else": {
                        "type": "ElseStatement",
                        "body": [
                            {
                                "type": "Assign",
                                "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                                "value": {"type": "Constant", "value": "3", "dtype": "NUMBER"},
                                "operator": "="
                            }
                        ],
                        "test": None
                    }
                }
            ]
        }
        result = parse_python(code)
        assert result == expected

    def test_nested_if(self):
        code = "if True:\n    if False:\n        x = 1"
        expected = {
            "type": "Module",
            "body": [
                {
                    "type": "IfStatement",
                    "test": {"type": "Constant", "value": True, "dtype": "BOOLEAN"},
                    "body": [
                        {
                            "type": "IfStatement",
                            "test": {"type": "Constant", "value": False, "dtype": "BOOLEAN"},
                            "body": [
                                {
                                    "type": "Assign",
                                    "targets": [{"type": "Name", "id": "x", "ctx": "Load"}],
                                    "value": {"type": "Constant", "value": "1", "dtype": "NUMBER"},
                                    "operator": "="
                                }
                            ],
                            "ifelse": None,
                            "else": None
                        }
                    ],
                    "ifelse": None,
                    "else": None
                }
            ]
        }
        result = parse_python(code)
        assert result == expected

    def test_complex_conditions(self):
        code = "if x > 1:\n    y = 2"
        expected = {
            "type": "Module",
            "body": [
                {
                    "type": "IfStatement",
                    "test": {
                        "type": "BinaryOp",
                        "left": {"type": "Name", "id": "x", "ctx": "Load"},
                        "operator": ">",
                        "right": {"type": "Constant", "value": "1", "dtype": "NUMBER"}
                    },
                    "body": [
                        {
                            "type": "Assign",
                            "targets": [{"type": "Name", "id": "y", "ctx": "Load"}],
                            "value": {"type": "Constant", "value": "2", "dtype": "NUMBER"},
                            "operator": "="
                        }
                    ],
                    "ifelse": None,
                    "else": None
                }
            ]
        }
        result = parse_python(code)
        assert result == expected
