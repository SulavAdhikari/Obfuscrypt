from antlr4 import *
from pyparser.PythonLexer import PythonLexer
from pyparser.PythonParser import PythonParser
from pyparser.python_ast_visitor import PythonASTVisitor
import json

def parse_python(code: str) -> dict:
    input_stream = InputStream(code)
    lexer = PythonLexer(input=input_stream)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    tree = parser.file_input()
    
    visitor = PythonASTVisitor()
    ast = visitor.visit(tree)
    return ast.to_dict()

# Example usage
if '__main__' == __name__:

    code = """

def addFunc(par1, par2):
    abc = par1 + par2
    return abc
    
bca = addFunc(12,78)

"""

    ast_dict = parse_python(code)
    print(json.dumps(ast_dict, indent=4))


"""

def abcvasdfasf(a123, b123):
    return a123 + b123

"""