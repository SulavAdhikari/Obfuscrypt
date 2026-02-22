from antlr4 import *
from antlr4.Token import CommonToken
from typing import List
import sys
import re

class PythonLexerBase(Lexer):
    def __init__(self, input: InputStream, output=sys.stdout):
        super().__init__(input, output)
        self.tokens: List[Token] = []
        self.indents: List[int] = []
        self.opened: int = 0
        self.last_token: Token = None

    def atStartOfInput(self) -> bool:
        return self.column == 0 and self.line == 1
    
    def reset(self):
        super().reset()
        self.tokens.clear()
        self.indents.clear()
        self.opened = 0
        self.last_token = None

    def nextToken(self) -> Token:
        # Return pending tokens first
        if self.tokens:
            return self.tokens.pop(0)

        token = super().nextToken()

        if token.type == Token.EOF:
            if self.indents:
                self.emit_token(self.LINE_BREAK, "\n")
                while self.indents:
                    self.indents.pop()
                    self.emit_token(self.DEDENT, "")
            if self.tokens:
                return self.tokens.pop(0)

        # The NEWLINE token (type == self.NEWLINE) is a raw ANTLR-matched token
        # that triggers onNewLine() via its action. onNewLine() already queues the
        # proper LINE_BREAK (and INDENT/DEDENT) into self.tokens. We must hide the
        # raw NEWLINE so it doesn't appear BEFORE LINE_BREAK in the token stream.
        if token.type == self.NEWLINE and self.tokens:
            # Hide the raw NEWLINE; the queued LINE_BREAK/INDENT/DEDENT will be
            # returned on the next calls.
            token.channel = Token.HIDDEN_CHANNEL
            self.last_token = token
            return self.nextToken()  # recurse to return the queued token

        self.last_token = token
        return token

    def emit_token(self, token_type: int, text: str = "") -> None:
        start = self.last_token.start if self.last_token else -1
        stop = self.last_token.stop if self.last_token else -1
        token = CommonToken(
            type=token_type,
            channel=Token.DEFAULT_CHANNEL,
            start=start,
            stop=stop
        )
        token.text = text
        self.tokens.append(token)

    def IncIndentLevel(self) -> None:
        self.opened += 1

    def DecIndentLevel(self) -> None:
        if self.opened > 0:
            self.opened -= 1

    def onNewLine(self):
        # self.text is e.g. '\n    ' — strip leading newline/CR chars before
        # measuring the indentation of the next line.
        stripped = self.text.lstrip('\r\n\f')
        spaces = re.match(r"[ \t]*", stripped).group(0)
        current_indent = len(spaces.replace("\t", "    "))  # tabs = 4 spaces

        # Emit LINE_BREAK first (the grammar expects LINE_BREAK before INDENT/DEDENT)
        self.emit_token(self.LINE_BREAK, self.text)

        if self.opened == 0:
            prev_indent = self.indents[-1] if self.indents else 0
            if current_indent > prev_indent:
                self.indents.append(current_indent)
                self.emit_token(self.INDENT)
            elif current_indent < prev_indent:
                while self.indents and current_indent < self.indents[-1]:
                    self.indents.pop()
                    self.emit_token(self.DEDENT)
