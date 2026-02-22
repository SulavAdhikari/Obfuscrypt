from pyparser.main import parse_python
import pytest


class TestLoops:

    # ── While loops ─────────────────────────────────────────────────────────

    def test_simple_while(self):
        """Simple while loop with a BinaryOp condition and an Assign body."""
        code = "while x > 0:\n    x = x - 1"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "WhileStatement"
        # condition is a BinaryOp
        assert body_0["test"]["type"] == "BinaryOp"
        assert body_0["test"]["operator"] == ">"
        # body contains an Assign
        assert body_0["body"][0]["type"] == "Assign"
        # no orelse
        assert body_0["orelse"] == []

    def test_while_with_else(self):
        """While loop with an else clause."""
        code = "while x > 0:\n    x = x - 1\nelse:\n    x = 99"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "WhileStatement"
        # orelse has the else-body Assign
        assert len(body_0["orelse"]) == 1
        assert body_0["orelse"][0]["type"] == "Assign"
        assert body_0["orelse"][0]["targets"][0]["id"] == "x"

    def test_nested_while_while(self):
        """Nested while loop inside another while loop."""
        code = "while x > 0:\n    while y > 0:\n        y = y - 1"
        result = parse_python(code)
        outer = result["body"][0]
        
        assert outer["type"] == "WhileStatement"
        inner = outer["body"][0]
        assert inner["type"] == "WhileStatement"
        assert inner["body"][0]["type"] == "Assign"
        
    def test_while_with_multiple_stmts_in_else(self):
        """While loop with multiple statements in the else clause."""
        code = "while False:\n    pass\nelse:\n    x = 1\n    y = 2"
        result = parse_python(code)
        body_0 = result["body"][0]
        
        assert body_0["type"] == "WhileStatement"
        assert len(body_0["orelse"]) == 2
        assert body_0["orelse"][0]["type"] == "Assign"
        assert body_0["orelse"][1]["type"] == "Assign"
        assert body_0["orelse"][0]["targets"][0]["id"] == "x"
        assert body_0["orelse"][1]["targets"][0]["id"] == "y"

    def test_while_empty_body_pass(self):
        """While loop with an empty body (pass)."""
        code = "while True:\n    pass"
        result = parse_python(code)
        body_0 = result["body"][0]
        
        assert body_0["type"] == "WhileStatement"
        assert len(body_0["body"]) == 1
        assert body_0["orelse"] == []

    # ── For loops ───────────────────────────────────────────────────────────

    def test_simple_for(self):
        """Simple for loop."""
        code = "for i in items:\n    x = i"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "ForStatement"
        assert body_0["target"]["type"] == "Name"
        assert body_0["target"]["id"] == "i"
        assert body_0["iter"]["type"] == "Name"
        assert body_0["iter"]["id"] == "items"
        assert body_0["body"][0]["type"] == "Assign"
        assert body_0["orelse"] == []

    def test_for_with_else(self):
        """For loop with else clause."""
        code = "for i in items:\n    x = i\nelse:\n    x = 0"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "ForStatement"
        assert len(body_0["orelse"]) == 1
        assert body_0["orelse"][0]["type"] == "Assign"

    def test_nested_for_while(self):
        """For loop containing a while loop."""
        code = "for i in items:\n    while x > 0:\n        x = x - 1"
        result = parse_python(code)
        outer = result["body"][0]

        assert outer["type"] == "ForStatement"
        assert isinstance(outer["orelse"], list)
        assert outer["orelse"] == []

    # ── break, continue, pass ───────────────────────────────────────────────

    def test_break_in_loop(self):
        """Break inside a while loop."""
        code = "while True:\n    break"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "WhileStatement"
        assert body_0["body"][0] == {"type": "Break"}

    def test_continue_in_loop(self):
        """Continue inside a for loop."""
        code = "for i in items:\n    continue"
        result = parse_python(code)
        body_0 = result["body"][0]

        assert body_0["type"] == "ForStatement"
        assert body_0["body"][0] == {"type": "Continue"}

    def test_pass_statement(self):
        """Pass inside a function body."""
        code = "def foo():\n    pass"
        result = parse_python(code)
        func_body = result["body"][0]["body"]

        assert func_body[0] == {"type": "Pass"}
