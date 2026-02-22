import pytest
from pyparser.main import parse_python
from pyparser.python_ast_visitor import PythonASTVisitor
from pyparser.PythonParser import PythonParser

class TestImports:
    def test_simple_import(self):
        code = "import os"
        result = parse_python(code)
        
        assert result["type"] == "Module"
        assert len(result["body"]) == 1
        
        stmt = result["body"][0]
        assert stmt["type"] == "Import"
        assert len(stmt["names"]) == 1
        
        name = stmt["names"][0]
        assert name["asname"] is None

    def test_import_alias(self):
        code = "import os as operating_system"
        result = parse_python(code)
        
        assert result["type"] == "Module"
        stmt = result["body"][0]
        assert stmt["type"] == "Import"
        name = stmt["names"][0]
        assert name["name"] == "os"
        assert name["asname"] == "operating_system"

    def test_from_import(self):
        code = "from os import path"
        result = parse_python(code)
        
        assert result["type"] == "Module"
        stmt = result["body"][0]
        assert stmt["type"] == "ImportFrom"
        assert stmt["module"] == "os"
        name = stmt["names"][0]
        assert name["asname"] is None

    def test_from_import_alias(self):
        code = "from os import path as p"
        result = parse_python(code)
        
        assert result["type"] == "Module"
        stmt = result["body"][0]
        assert stmt["type"] == "ImportFrom"
        assert stmt["module"] == "os"
        name = stmt["names"][0]
        assert name["name"] == "path"
        assert name["asname"] == "p"

    def test_multiple_imports(self):
        code = "from os import path, getcwd"
        result = parse_python(code)
        
        assert result["type"] == "Module"
        stmt = result["body"][0]
        assert stmt["type"] == "ImportFrom"
        assert len(stmt["names"]) == 2
        assert stmt["names"][0]["name"] == "path"
        assert stmt["names"][1]["name"] == "getcwd"
