from antlr4 import *
from pyparser.PythonLexer import PythonLexer
from pyparser.PythonParser import PythonParser
from pyparser.python_ast_visitor import PythonASTVisitor
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(BASE_DIR, 'input')
output_folder = os.path.join(BASE_DIR, 'output')

input_file = open(os.path.join(input_folder, 'input.py'), 'rt')
output_file = open(os.path.join(output_folder, 'output.json'), 'wt')

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

    code = input_file.read()
    input_file.close()
    ast_dict = parse_python(code)
    output_file.write(json.dumps(ast_dict, indent=4))
    output_file.close()


