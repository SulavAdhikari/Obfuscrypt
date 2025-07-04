# Generated from ./powerparser/PowerExp.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PowerExpParser import PowerExpParser
else:
    from PowerExpParser import PowerExpParser

# This class defines a complete generic visitor for a parse tree produced by PowerExpParser.

class PowerExpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PowerExpParser#script.
    def visitScript(self, ctx:PowerExpParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#codeBlock.
    def visitCodeBlock(self, ctx:PowerExpParser.CodeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#codeBlockStatements.
    def visitCodeBlockStatements(self, ctx:PowerExpParser.CodeBlockStatementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#statement.
    def visitStatement(self, ctx:PowerExpParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#commandName.
    def visitCommandName(self, ctx:PowerExpParser.CommandNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#commandStatement.
    def visitCommandStatement(self, ctx:PowerExpParser.CommandStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#argument.
    def visitArgument(self, ctx:PowerExpParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#typeCast.
    def visitTypeCast(self, ctx:PowerExpParser.TypeCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#assignment.
    def visitAssignment(self, ctx:PowerExpParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#assignee.
    def visitAssignee(self, ctx:PowerExpParser.AssigneeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#operator.
    def visitOperator(self, ctx:PowerExpParser.OperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#ifStatement.
    def visitIfStatement(self, ctx:PowerExpParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#foreachStatement.
    def visitForeachStatement(self, ctx:PowerExpParser.ForeachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:PowerExpParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#functionName.
    def visitFunctionName(self, ctx:PowerExpParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#functionCall.
    def visitFunctionCall(self, ctx:PowerExpParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#functionDecl.
    def visitFunctionDecl(self, ctx:PowerExpParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PowerExpParser#memberAccess.
    def visitMemberAccess(self, ctx:PowerExpParser.MemberAccessContext):
        return self.visitChildren(ctx)



del PowerExpParser