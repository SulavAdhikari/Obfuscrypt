# Generated from ./powerparser/PowerExp.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PowerExpParser import PowerExpParser
else:
    from PowerExpParser import PowerExpParser

# This class defines a complete listener for a parse tree produced by PowerExpParser.
class PowerExpListener(ParseTreeListener):

    # Enter a parse tree produced by PowerExpParser#script.
    def enterScript(self, ctx:PowerExpParser.ScriptContext):
        pass

    # Exit a parse tree produced by PowerExpParser#script.
    def exitScript(self, ctx:PowerExpParser.ScriptContext):
        pass


    # Enter a parse tree produced by PowerExpParser#codeBlock.
    def enterCodeBlock(self, ctx:PowerExpParser.CodeBlockContext):
        pass

    # Exit a parse tree produced by PowerExpParser#codeBlock.
    def exitCodeBlock(self, ctx:PowerExpParser.CodeBlockContext):
        pass


    # Enter a parse tree produced by PowerExpParser#codeBlockStatements.
    def enterCodeBlockStatements(self, ctx:PowerExpParser.CodeBlockStatementsContext):
        pass

    # Exit a parse tree produced by PowerExpParser#codeBlockStatements.
    def exitCodeBlockStatements(self, ctx:PowerExpParser.CodeBlockStatementsContext):
        pass


    # Enter a parse tree produced by PowerExpParser#statement.
    def enterStatement(self, ctx:PowerExpParser.StatementContext):
        pass

    # Exit a parse tree produced by PowerExpParser#statement.
    def exitStatement(self, ctx:PowerExpParser.StatementContext):
        pass


    # Enter a parse tree produced by PowerExpParser#commandName.
    def enterCommandName(self, ctx:PowerExpParser.CommandNameContext):
        pass

    # Exit a parse tree produced by PowerExpParser#commandName.
    def exitCommandName(self, ctx:PowerExpParser.CommandNameContext):
        pass


    # Enter a parse tree produced by PowerExpParser#commandStatement.
    def enterCommandStatement(self, ctx:PowerExpParser.CommandStatementContext):
        pass

    # Exit a parse tree produced by PowerExpParser#commandStatement.
    def exitCommandStatement(self, ctx:PowerExpParser.CommandStatementContext):
        pass


    # Enter a parse tree produced by PowerExpParser#argument.
    def enterArgument(self, ctx:PowerExpParser.ArgumentContext):
        pass

    # Exit a parse tree produced by PowerExpParser#argument.
    def exitArgument(self, ctx:PowerExpParser.ArgumentContext):
        pass


    # Enter a parse tree produced by PowerExpParser#typeCast.
    def enterTypeCast(self, ctx:PowerExpParser.TypeCastContext):
        pass

    # Exit a parse tree produced by PowerExpParser#typeCast.
    def exitTypeCast(self, ctx:PowerExpParser.TypeCastContext):
        pass


    # Enter a parse tree produced by PowerExpParser#assignment.
    def enterAssignment(self, ctx:PowerExpParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PowerExpParser#assignment.
    def exitAssignment(self, ctx:PowerExpParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PowerExpParser#assignee.
    def enterAssignee(self, ctx:PowerExpParser.AssigneeContext):
        pass

    # Exit a parse tree produced by PowerExpParser#assignee.
    def exitAssignee(self, ctx:PowerExpParser.AssigneeContext):
        pass


    # Enter a parse tree produced by PowerExpParser#operator.
    def enterOperator(self, ctx:PowerExpParser.OperatorContext):
        pass

    # Exit a parse tree produced by PowerExpParser#operator.
    def exitOperator(self, ctx:PowerExpParser.OperatorContext):
        pass


    # Enter a parse tree produced by PowerExpParser#ifStatement.
    def enterIfStatement(self, ctx:PowerExpParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PowerExpParser#ifStatement.
    def exitIfStatement(self, ctx:PowerExpParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PowerExpParser#foreachStatement.
    def enterForeachStatement(self, ctx:PowerExpParser.ForeachStatementContext):
        pass

    # Exit a parse tree produced by PowerExpParser#foreachStatement.
    def exitForeachStatement(self, ctx:PowerExpParser.ForeachStatementContext):
        pass


    # Enter a parse tree produced by PowerExpParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:PowerExpParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by PowerExpParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:PowerExpParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by PowerExpParser#functionName.
    def enterFunctionName(self, ctx:PowerExpParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by PowerExpParser#functionName.
    def exitFunctionName(self, ctx:PowerExpParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by PowerExpParser#functionCall.
    def enterFunctionCall(self, ctx:PowerExpParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by PowerExpParser#functionCall.
    def exitFunctionCall(self, ctx:PowerExpParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by PowerExpParser#functionDecl.
    def enterFunctionDecl(self, ctx:PowerExpParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by PowerExpParser#functionDecl.
    def exitFunctionDecl(self, ctx:PowerExpParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by PowerExpParser#memberAccess.
    def enterMemberAccess(self, ctx:PowerExpParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by PowerExpParser#memberAccess.
    def exitMemberAccess(self, ctx:PowerExpParser.MemberAccessContext):
        pass



del PowerExpParser