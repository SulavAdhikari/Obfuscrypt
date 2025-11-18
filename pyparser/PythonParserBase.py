from antlr4 import Parser
from typing import List
import sys

class PythonParserBase(Parser):
    def __init__(self, input, output = sys.stdout):
        super().__init__(input, output= sys.stdout)
        self._python_version = 3

    def CheckVersion(self, version: int) -> bool:
        return self._python_version == version

    def SetVersion(self, version: int) -> None:
        self._python_version = version

    def IsVersion2(self) -> bool:
        return self._python_version == 2

    def IsVersion3(self) -> bool:
        return self._python_version == 3