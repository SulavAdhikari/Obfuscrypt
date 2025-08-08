from antlr4 import *
from typing import List

class PythonLexerBase(Lexer):
    def __init__(self, input: InputStream):
        super().__init__(input)
        self.tokens: List[Token] = []
        self.indents: List[int] = []
        self.opened: int = 0
        self.last_token = None
        self.first_token = True

    def reset(self):
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.last_token = None
        self.first_token = True
        super().reset()

    def nextToken(self) -> Token:
        if self.tokens:
            next_token = self.tokens.pop(0)
            return next_token

        token = super().nextToken()

        if token.type == Token.EOF and self.indents:
            self.emit_token(self.NEWLINE)
            while self.indents:
                self.emit_token(self.DEDENT)
                self.indents.pop()

        self.last_token = token
        return token

    def emit_token(self, token_type: int) -> None:
        token = CommonToken(
            type=token_type,
            channel=Token.DEFAULT_CHANNEL,
            text="",
            start=self.last_token.start if self.last_token else 0,
            stop=self.last_token.stop if self.last_token else 0
        )
        self.tokens.append(token)

    def IncIndentLevel(self) -> None:
        self.opened += 1

    def DecIndentLevel(self) -> None:
        if self.opened > 0:
            self.opened -= 1

    def atStartOfInput(self) -> bool:
        return self.first_token

    def onNewLine(self) -> None:
        self.first_token = False
        newLine = self.text.replace(" ", "").replace("\t", "")
        spaces = self.text.replace("\r", "").replace("\n", "").replace("\f", "")

        if self.opened == 0:
            if len(spaces) > 0:
                current_indent = len(spaces)
                if not self.indents or current_indent > self.indents[-1]:
                    self.indents.append(current_indent)
                    self.emit_token(self.INDENT)
                elif current_indent < self.indents[-1]:
                    while self.indents and current_indent < self.indents[-1]:
                        self.emit_token(self.DEDENT)
                        self.indents.pop()

        if len(newLine) > 0:
            self.emit_token(self.NEWLINE)