# Generated from ./powerparser/PowerExp.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,32,167,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,1,0,1,0,5,0,40,8,0,10,
        0,12,0,43,9,0,1,0,1,0,1,1,1,1,1,1,5,1,50,8,1,10,1,12,1,53,9,1,1,
        2,1,2,1,2,1,2,1,2,3,2,60,8,2,1,3,1,3,1,3,1,3,1,3,1,3,3,3,68,8,3,
        1,4,1,4,1,5,1,5,5,5,74,8,5,10,5,12,5,77,9,5,1,6,1,6,1,6,1,6,1,6,
        3,6,84,8,6,1,7,1,7,1,7,1,7,3,7,90,8,7,1,7,1,7,1,8,1,8,1,8,1,8,1,
        9,3,9,99,8,9,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,3,11,117,8,11,1,12,1,12,1,12,1,12,1,12,
        1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,3,13,135,
        8,13,1,14,1,14,1,15,1,15,1,15,1,15,1,15,5,15,144,8,15,10,15,12,15,
        147,9,15,3,15,149,8,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,16,1,
        17,1,17,1,17,5,17,162,8,17,10,17,12,17,165,9,17,1,17,0,0,18,0,2,
        4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,0,3,1,0,30,31,1,0,28,
        29,1,0,4,13,175,0,41,1,0,0,0,2,51,1,0,0,0,4,59,1,0,0,0,6,67,1,0,
        0,0,8,69,1,0,0,0,10,71,1,0,0,0,12,83,1,0,0,0,14,85,1,0,0,0,16,93,
        1,0,0,0,18,98,1,0,0,0,20,102,1,0,0,0,22,104,1,0,0,0,24,118,1,0,0,
        0,26,134,1,0,0,0,28,136,1,0,0,0,30,138,1,0,0,0,32,152,1,0,0,0,34,
        158,1,0,0,0,36,37,3,6,3,0,37,38,7,0,0,0,38,40,1,0,0,0,39,36,1,0,
        0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,44,1,0,0,0,43,41,
        1,0,0,0,44,45,5,0,0,1,45,1,1,0,0,0,46,47,3,6,3,0,47,48,7,0,0,0,48,
        50,1,0,0,0,49,46,1,0,0,0,50,53,1,0,0,0,51,49,1,0,0,0,51,52,1,0,0,
        0,52,3,1,0,0,0,53,51,1,0,0,0,54,60,3,10,5,0,55,60,3,30,15,0,56,60,
        3,16,8,0,57,60,3,22,11,0,58,60,3,24,12,0,59,54,1,0,0,0,59,55,1,0,
        0,0,59,56,1,0,0,0,59,57,1,0,0,0,59,58,1,0,0,0,60,5,1,0,0,0,61,68,
        3,10,5,0,62,68,3,30,15,0,63,68,3,16,8,0,64,68,3,22,11,0,65,68,3,
        24,12,0,66,68,3,32,16,0,67,61,1,0,0,0,67,62,1,0,0,0,67,63,1,0,0,
        0,67,64,1,0,0,0,67,65,1,0,0,0,67,66,1,0,0,0,68,7,1,0,0,0,69,70,7,
        1,0,0,70,9,1,0,0,0,71,75,3,8,4,0,72,74,3,26,13,0,73,72,1,0,0,0,74,
        77,1,0,0,0,75,73,1,0,0,0,75,76,1,0,0,0,76,11,1,0,0,0,77,75,1,0,0,
        0,78,84,3,30,15,0,79,84,5,25,0,0,80,84,5,27,0,0,81,84,5,26,0,0,82,
        84,5,28,0,0,83,78,1,0,0,0,83,79,1,0,0,0,83,80,1,0,0,0,83,81,1,0,
        0,0,83,82,1,0,0,0,84,13,1,0,0,0,85,86,5,1,0,0,86,89,5,28,0,0,87,
        88,5,1,0,0,88,90,5,2,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,91,1,0,0,
        0,91,92,5,2,0,0,92,15,1,0,0,0,93,94,3,18,9,0,94,95,5,3,0,0,95,96,
        3,26,13,0,96,17,1,0,0,0,97,99,3,14,7,0,98,97,1,0,0,0,98,99,1,0,0,
        0,99,100,1,0,0,0,100,101,5,27,0,0,101,19,1,0,0,0,102,103,7,2,0,0,
        103,21,1,0,0,0,104,105,5,14,0,0,105,106,5,15,0,0,106,107,3,26,13,
        0,107,108,5,16,0,0,108,109,5,17,0,0,109,110,3,2,1,0,110,116,5,18,
        0,0,111,112,5,19,0,0,112,113,5,17,0,0,113,114,3,2,1,0,114,115,5,
        18,0,0,115,117,1,0,0,0,116,111,1,0,0,0,116,117,1,0,0,0,117,23,1,
        0,0,0,118,119,5,20,0,0,119,120,5,15,0,0,120,121,5,27,0,0,121,122,
        5,21,0,0,122,123,3,26,13,0,123,124,5,16,0,0,124,125,5,17,0,0,125,
        126,3,2,1,0,126,127,5,18,0,0,127,25,1,0,0,0,128,135,3,34,17,0,129,
        135,3,30,15,0,130,135,3,10,5,0,131,135,5,25,0,0,132,135,5,26,0,0,
        133,135,5,27,0,0,134,128,1,0,0,0,134,129,1,0,0,0,134,130,1,0,0,0,
        134,131,1,0,0,0,134,132,1,0,0,0,134,133,1,0,0,0,135,27,1,0,0,0,136,
        137,5,28,0,0,137,29,1,0,0,0,138,139,3,28,14,0,139,148,5,15,0,0,140,
        145,3,12,6,0,141,142,5,22,0,0,142,144,3,12,6,0,143,141,1,0,0,0,144,
        147,1,0,0,0,145,143,1,0,0,0,145,146,1,0,0,0,146,149,1,0,0,0,147,
        145,1,0,0,0,148,140,1,0,0,0,148,149,1,0,0,0,149,150,1,0,0,0,150,
        151,5,16,0,0,151,31,1,0,0,0,152,153,5,23,0,0,153,154,3,28,14,0,154,
        155,5,17,0,0,155,156,3,2,1,0,156,157,5,18,0,0,157,33,1,0,0,0,158,
        163,3,12,6,0,159,160,5,24,0,0,160,162,3,12,6,0,161,159,1,0,0,0,162,
        165,1,0,0,0,163,161,1,0,0,0,163,164,1,0,0,0,164,35,1,0,0,0,165,163,
        1,0,0,0,13,41,51,59,67,75,83,89,98,116,134,145,148,163
    ]

class PowerExpParser ( Parser ):

    grammarFileName = "PowerExp.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'='", "'+'", "'-'", "'*'", 
                     "'/'", "'-eq'", "'-ne'", "'-gt'", "'-lt'", "'-and'", 
                     "'-or'", "'if'", "'('", "')'", "'{'", "'}'", "'else'", 
                     "'foreach'", "'in'", "','", "'function'", "'.'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "';'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "STRING", "NUMBER", "VARIABLE", "IDENTIFIER", 
                      "COMMAND_NAME", "NEWLINE", "SEMICOLON", "WS" ]

    RULE_script = 0
    RULE_codeBlock = 1
    RULE_codeBlockStatements = 2
    RULE_statement = 3
    RULE_commandName = 4
    RULE_commandStatement = 5
    RULE_argument = 6
    RULE_typeCast = 7
    RULE_assignment = 8
    RULE_assignee = 9
    RULE_operator = 10
    RULE_ifStatement = 11
    RULE_foreachStatement = 12
    RULE_primaryExpression = 13
    RULE_functionName = 14
    RULE_functionCall = 15
    RULE_functionDecl = 16
    RULE_memberAccess = 17

    ruleNames =  [ "script", "codeBlock", "codeBlockStatements", "statement", 
                   "commandName", "commandStatement", "argument", "typeCast", 
                   "assignment", "assignee", "operator", "ifStatement", 
                   "foreachStatement", "primaryExpression", "functionName", 
                   "functionCall", "functionDecl", "memberAccess" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    STRING=25
    NUMBER=26
    VARIABLE=27
    IDENTIFIER=28
    COMMAND_NAME=29
    NEWLINE=30
    SEMICOLON=31
    WS=32

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ScriptContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PowerExpParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.StatementContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.StatementContext,i)


        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(PowerExpParser.SEMICOLON)
            else:
                return self.getToken(PowerExpParser.SEMICOLON, i)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PowerExpParser.NEWLINE)
            else:
                return self.getToken(PowerExpParser.NEWLINE, i)

        def getRuleIndex(self):
            return PowerExpParser.RULE_script

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterScript" ):
                listener.enterScript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitScript" ):
                listener.exitScript(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitScript" ):
                return visitor.visitScript(self)
            else:
                return visitor.visitChildren(self)




    def script(self):

        localctx = PowerExpParser.ScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_script)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 948977666) != 0):
                self.state = 36
                self.statement()
                self.state = 37
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
            self.match(PowerExpParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CodeBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.StatementContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.StatementContext,i)


        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(PowerExpParser.SEMICOLON)
            else:
                return self.getToken(PowerExpParser.SEMICOLON, i)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PowerExpParser.NEWLINE)
            else:
                return self.getToken(PowerExpParser.NEWLINE, i)

        def getRuleIndex(self):
            return PowerExpParser.RULE_codeBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCodeBlock" ):
                listener.enterCodeBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCodeBlock" ):
                listener.exitCodeBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCodeBlock" ):
                return visitor.visitCodeBlock(self)
            else:
                return visitor.visitChildren(self)




    def codeBlock(self):

        localctx = PowerExpParser.CodeBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_codeBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 948977666) != 0):
                self.state = 46
                self.statement()
                self.state = 47
                _la = self._input.LA(1)
                if not(_la==30 or _la==31):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CodeBlockStatementsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def commandStatement(self):
            return self.getTypedRuleContext(PowerExpParser.CommandStatementContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionCallContext,0)


        def assignment(self):
            return self.getTypedRuleContext(PowerExpParser.AssignmentContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(PowerExpParser.IfStatementContext,0)


        def foreachStatement(self):
            return self.getTypedRuleContext(PowerExpParser.ForeachStatementContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_codeBlockStatements

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCodeBlockStatements" ):
                listener.enterCodeBlockStatements(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCodeBlockStatements" ):
                listener.exitCodeBlockStatements(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCodeBlockStatements" ):
                return visitor.visitCodeBlockStatements(self)
            else:
                return visitor.visitChildren(self)




    def codeBlockStatements(self):

        localctx = PowerExpParser.CodeBlockStatementsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_codeBlockStatements)
        try:
            self.state = 59
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.commandStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.functionCall()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 57
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 58
                self.foreachStatement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def commandStatement(self):
            return self.getTypedRuleContext(PowerExpParser.CommandStatementContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionCallContext,0)


        def assignment(self):
            return self.getTypedRuleContext(PowerExpParser.AssignmentContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(PowerExpParser.IfStatementContext,0)


        def foreachStatement(self):
            return self.getTypedRuleContext(PowerExpParser.ForeachStatementContext,0)


        def functionDecl(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionDeclContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = PowerExpParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_statement)
        try:
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 61
                self.commandStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 62
                self.functionCall()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 64
                self.ifStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 65
                self.foreachStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 66
                self.functionDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMAND_NAME(self):
            return self.getToken(PowerExpParser.COMMAND_NAME, 0)

        def IDENTIFIER(self):
            return self.getToken(PowerExpParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return PowerExpParser.RULE_commandName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommandName" ):
                listener.enterCommandName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommandName" ):
                listener.exitCommandName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommandName" ):
                return visitor.visitCommandName(self)
            else:
                return visitor.visitChildren(self)




    def commandName(self):

        localctx = PowerExpParser.CommandNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_commandName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            _la = self._input.LA(1)
            if not(_la==28 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def commandName(self):
            return self.getTypedRuleContext(PowerExpParser.CommandNameContext,0)


        def primaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.PrimaryExpressionContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.PrimaryExpressionContext,i)


        def getRuleIndex(self):
            return PowerExpParser.RULE_commandStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommandStatement" ):
                listener.enterCommandStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommandStatement" ):
                listener.exitCommandStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommandStatement" ):
                return visitor.visitCommandStatement(self)
            else:
                return visitor.visitChildren(self)




    def commandStatement(self):

        localctx = PowerExpParser.CommandStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_commandStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.commandName()
            self.state = 75
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 72
                    self.primaryExpression() 
                self.state = 77
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionCall(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionCallContext,0)


        def STRING(self):
            return self.getToken(PowerExpParser.STRING, 0)

        def VARIABLE(self):
            return self.getToken(PowerExpParser.VARIABLE, 0)

        def NUMBER(self):
            return self.getToken(PowerExpParser.NUMBER, 0)

        def IDENTIFIER(self):
            return self.getToken(PowerExpParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return PowerExpParser.RULE_argument

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgument" ):
                listener.enterArgument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgument" ):
                listener.exitArgument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgument" ):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = PowerExpParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_argument)
        try:
            self.state = 83
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 78
                self.functionCall()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.match(PowerExpParser.STRING)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.match(PowerExpParser.VARIABLE)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.match(PowerExpParser.NUMBER)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 82
                self.match(PowerExpParser.IDENTIFIER)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeCastContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(PowerExpParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return PowerExpParser.RULE_typeCast

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeCast" ):
                listener.enterTypeCast(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeCast" ):
                listener.exitTypeCast(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeCast" ):
                return visitor.visitTypeCast(self)
            else:
                return visitor.visitChildren(self)




    def typeCast(self):

        localctx = PowerExpParser.TypeCastContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeCast)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.match(PowerExpParser.T__0)
            self.state = 86
            self.match(PowerExpParser.IDENTIFIER)
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 87
                self.match(PowerExpParser.T__0)
                self.state = 88
                self.match(PowerExpParser.T__1)


            self.state = 91
            self.match(PowerExpParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignee(self):
            return self.getTypedRuleContext(PowerExpParser.AssigneeContext,0)


        def primaryExpression(self):
            return self.getTypedRuleContext(PowerExpParser.PrimaryExpressionContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = PowerExpParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.assignee()
            self.state = 94
            self.match(PowerExpParser.T__2)
            self.state = 95
            self.primaryExpression()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssigneeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE(self):
            return self.getToken(PowerExpParser.VARIABLE, 0)

        def typeCast(self):
            return self.getTypedRuleContext(PowerExpParser.TypeCastContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_assignee

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignee" ):
                listener.enterAssignee(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignee" ):
                listener.exitAssignee(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignee" ):
                return visitor.visitAssignee(self)
            else:
                return visitor.visitChildren(self)




    def assignee(self):

        localctx = PowerExpParser.AssigneeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_assignee)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 97
                self.typeCast()


            self.state = 100
            self.match(PowerExpParser.VARIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return PowerExpParser.RULE_operator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperator" ):
                listener.enterOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperator" ):
                listener.exitOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperator" ):
                return visitor.visitOperator(self)
            else:
                return visitor.visitChildren(self)




    def operator(self):

        localctx = PowerExpParser.OperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_operator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16368) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primaryExpression(self):
            return self.getTypedRuleContext(PowerExpParser.PrimaryExpressionContext,0)


        def codeBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.CodeBlockContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.CodeBlockContext,i)


        def getRuleIndex(self):
            return PowerExpParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = PowerExpParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_ifStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(PowerExpParser.T__13)
            self.state = 105
            self.match(PowerExpParser.T__14)
            self.state = 106
            self.primaryExpression()
            self.state = 107
            self.match(PowerExpParser.T__15)
            self.state = 108
            self.match(PowerExpParser.T__16)
            self.state = 109
            self.codeBlock()
            self.state = 110
            self.match(PowerExpParser.T__17)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 111
                self.match(PowerExpParser.T__18)
                self.state = 112
                self.match(PowerExpParser.T__16)
                self.state = 113
                self.codeBlock()
                self.state = 114
                self.match(PowerExpParser.T__17)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForeachStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE(self):
            return self.getToken(PowerExpParser.VARIABLE, 0)

        def primaryExpression(self):
            return self.getTypedRuleContext(PowerExpParser.PrimaryExpressionContext,0)


        def codeBlock(self):
            return self.getTypedRuleContext(PowerExpParser.CodeBlockContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_foreachStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForeachStatement" ):
                listener.enterForeachStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForeachStatement" ):
                listener.exitForeachStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForeachStatement" ):
                return visitor.visitForeachStatement(self)
            else:
                return visitor.visitChildren(self)




    def foreachStatement(self):

        localctx = PowerExpParser.ForeachStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_foreachStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(PowerExpParser.T__19)
            self.state = 119
            self.match(PowerExpParser.T__14)
            self.state = 120
            self.match(PowerExpParser.VARIABLE)
            self.state = 121
            self.match(PowerExpParser.T__20)
            self.state = 122
            self.primaryExpression()
            self.state = 123
            self.match(PowerExpParser.T__15)
            self.state = 124
            self.match(PowerExpParser.T__16)
            self.state = 125
            self.codeBlock()
            self.state = 126
            self.match(PowerExpParser.T__17)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def memberAccess(self):
            return self.getTypedRuleContext(PowerExpParser.MemberAccessContext,0)


        def functionCall(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionCallContext,0)


        def commandStatement(self):
            return self.getTypedRuleContext(PowerExpParser.CommandStatementContext,0)


        def STRING(self):
            return self.getToken(PowerExpParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(PowerExpParser.NUMBER, 0)

        def VARIABLE(self):
            return self.getToken(PowerExpParser.VARIABLE, 0)

        def getRuleIndex(self):
            return PowerExpParser.RULE_primaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpression" ):
                listener.enterPrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpression" ):
                listener.exitPrimaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = PowerExpParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_primaryExpression)
        try:
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 128
                self.memberAccess()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 129
                self.functionCall()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 130
                self.commandStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 131
                self.match(PowerExpParser.STRING)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 132
                self.match(PowerExpParser.NUMBER)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 133
                self.match(PowerExpParser.VARIABLE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(PowerExpParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return PowerExpParser.RULE_functionName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionName" ):
                listener.enterFunctionName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionName" ):
                listener.exitFunctionName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionName" ):
                return visitor.visitFunctionName(self)
            else:
                return visitor.visitChildren(self)




    def functionName(self):

        localctx = PowerExpParser.FunctionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_functionName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(PowerExpParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionName(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionNameContext,0)


        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.ArgumentContext,i)


        def getRuleIndex(self):
            return PowerExpParser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = PowerExpParser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.functionName()
            self.state = 139
            self.match(PowerExpParser.T__14)
            self.state = 148
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 503316480) != 0):
                self.state = 140
                self.argument()
                self.state = 145
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==22:
                    self.state = 141
                    self.match(PowerExpParser.T__21)
                    self.state = 142
                    self.argument()
                    self.state = 147
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 150
            self.match(PowerExpParser.T__15)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionName(self):
            return self.getTypedRuleContext(PowerExpParser.FunctionNameContext,0)


        def codeBlock(self):
            return self.getTypedRuleContext(PowerExpParser.CodeBlockContext,0)


        def getRuleIndex(self):
            return PowerExpParser.RULE_functionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDecl" ):
                listener.enterFunctionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDecl" ):
                listener.exitFunctionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDecl" ):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)




    def functionDecl(self):

        localctx = PowerExpParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_functionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.match(PowerExpParser.T__22)
            self.state = 153
            self.functionName()
            self.state = 154
            self.match(PowerExpParser.T__16)
            self.state = 155
            self.codeBlock()
            self.state = 156
            self.match(PowerExpParser.T__17)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MemberAccessContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PowerExpParser.ArgumentContext)
            else:
                return self.getTypedRuleContext(PowerExpParser.ArgumentContext,i)


        def getRuleIndex(self):
            return PowerExpParser.RULE_memberAccess

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberAccess" ):
                listener.enterMemberAccess(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberAccess" ):
                listener.exitMemberAccess(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberAccess" ):
                return visitor.visitMemberAccess(self)
            else:
                return visitor.visitChildren(self)




    def memberAccess(self):

        localctx = PowerExpParser.MemberAccessContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_memberAccess)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.argument()
            self.state = 163
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 159
                self.match(PowerExpParser.T__23)
                self.state = 160
                self.argument()
                self.state = 165
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





