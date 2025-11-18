from antlr4 import *
from pyparser.PythonParser import PythonParser
from pyparser.PythonParserVisitor import PythonParserVisitor
from obfuscrypt_base.ast_nodes import *

class PythonASTVisitor(PythonParserVisitor):

    # Top-level module node from file_input
    def visitFile_input(self, ctx: PythonParser.File_inputContext) -> Module:
        body = []
        stmts = ctx.getChildren()
        for stmt in stmts:
            node = self.visit(stmt)
            if node:
                # if isinstance(node, list):  # in case suite returns list of stmts
                #     body.extend(node)
                #else:
                body.append(node)
        return Module(node_type=NodeType.MODULE, body=body)

    # Function definition
    def visitFuncdef(self, ctx: PythonParser.FuncdefContext) -> FunctionDef:
        name = ctx.name().getText()
        args = self.visit(ctx.typedargslist()) if ctx.typedargslist() else Arguments(node_type=NodeType.ARGUMENTS, args=[], vararg=None, kwarg=None, defaults=[])
        returns = self.visit(ctx.test()) if ctx.test() else None
        body = self.visit(ctx.suite())
        async_ = bool(ctx.ASYNC())
        # decorators ignored for now, you can add later if ctx.decorator()
        return FunctionDef(
            node_type=NodeType.FUNCTION_DEF,
            name=name,
            args=args,
            body=body,
            decorator_list=[],
            returns=returns,
            async_=async_
        )

    # Typed args list for function arguments
    def visitTypedargslist(self, ctx: PythonParser.TypedargslistContext) -> Arguments:
        args = []
        vararg = None
        kwarg = None
        defaults = []

        # ctx can contain multiple children (arguments, varargs, kwargs, defaults)
        # Simplified parsing: just parse normal args and ignore complicated defaults for now
        # You should extend to cover all cases

        for child in ctx.getChildren():
            # Look for plain args (name nodes)
            if isinstance(child, PythonParser.Named_parameterContext):
                arg = self.visit(child)
                if arg:
                    args.append(arg)
            elif isinstance(child, PythonParser.VarargsContext):
                vararg = self.visit(child)
            elif isinstance(child, PythonParser.VarkwargsContext):
                kwarg = self.visit(child)
            elif isinstance(child, PythonParser.Def_parametersContext):
                # could be defaults, skip for now
                defaults = self.visit(child)

        return Arguments(node_type=NodeType.ARGUMENTS, args=args, vararg=vararg, kwarg=kwarg, defaults=defaults)

    def visitName(self, ctx):
        name = ctx.getText()
        if name == "True":
            return Constant(node_type=NodeType.CONSTANT, value=True, kind="BOOLEAN")
        elif name == "False":
            return Constant(node_type=NodeType.CONSTANT, value=False, kind="BOOLEAN")
        else:
            return Constant(node_type=NodeType.NAME, value=name)    
    
    def visitNamed_parameter(self, ctx: PythonParser.Named_parameterContext) -> Arg:
        name = ctx.name().getText()
        annotation = self.visit(ctx.test()) if ctx.test() else None
        return Arg(name=name, annotation=annotation)

    def visitVarargs(self, ctx: PythonParser.VarargsContext) -> Arg:
        # *args parameter
        name = ctx.name().getText()
        return Arg(name=name, annotation=None)

    def visitVarkwargs(self, ctx: PythonParser.VarkwargsContext) -> Arg:
        # **kwargs parameter
        name = ctx.name().getText()
        return Arg(name=name, annotation=None)

    # Suite (block of statements)
    def visitSuite(self, ctx: PythonParser.SuiteContext) -> List[Statement]:
        # suite can be a simple_stmt or a NEWLINE INDENT stmt+ DEDENT
        if ctx.simple_stmt():
            node = self.visit(ctx.simple_stmt())
            return [node] if node else []
        else:
            stmts = []
            for stmt in ctx.getChildren():
                node = self.visit(stmt)
                if node:
                    if isinstance(node, list):
                        stmts.extend(node)
                    else:
                        stmts.append(node)
            return stmts

    # Statement (dispatch to specific statements)
    def visitStmt(self, ctx: PythonParser.StmtContext) -> Statement:
        # stmt can be simple_stmt or compound_stmt
        if ctx.simple_stmt():
            return self.visit(ctx.simple_stmt())
        elif ctx.compound_stmt():
            return self.visit(ctx.compound_stmt())
        return None

    # Simple statements
    def visitSimple_stmt(self, ctx: PythonParser.Simple_stmtContext) -> Statement:
        # simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
        # Only visit the first small_stmt for now
        return self.visit(ctx.small_stmt(0))

    # Small statements dispatch
    def visitSmall_stmt(self, ctx):
        # This depends on your grammar, could be expr_stmt, return_stmt, etc
        if ctx.expr_stmt():
            return self.visit(ctx.expr_stmt())
        elif ctx.return_stmt():
            return self.visit(ctx.return_stmt())
        elif ctx.pass_stmt():
            return "pass"  # skip
        elif ctx.break_stmt():
            return None  # implement if you want
        elif ctx.continue_stmt():
            return None
        # add more as needed
        return None

    def visitExpr_stmt(self, ctx: PythonParser.Expr_stmtContext) -> Statement:
        # Check if assignment token exists
        if ctx.assign_part():
            # Left side is testlist(0), right side is testlist(1)
            targets = self.visit(ctx.testlist_star_expr())
            operator, value = self.visit(ctx.assign_part())
            # Wrap targets into list if needed
            if not isinstance(targets, list):
                targets = [targets]
            return Assign(node_type=NodeType.ASSIGN, targets=targets, value=value, operator=operator)
        else:
            # Just expression
            expr = self.visitChildren(ctx)
            return expr

    def visitAssign_part(self, ctx):
        operator = self.visit(ctx.getChild(0))
        value = self.visit(ctx.getChild(1))
        return operator, value
    
    def visitReturn_stmt(self, ctx: PythonParser.Return_stmtContext) -> Statement:
        expr = self.visit(ctx.testlist()) if ctx.testlist() else None
        return ReturnStmt(node_type=NodeType.RETURN, value=expr)

    # Function call
    def visitAtom(self, ctx: PythonParser.AtomContext) -> Expression:
            # This is a function call
        atom_node = None
        if ctx.name():
            atom_node = Name(node_type=NodeType.NAME, id=ctx.name().getText(), ctx='Load')
        elif ctx.number():
            atom_node = Constant(node_type=NodeType.CONSTANT, value=ctx.number().getText(), dtype="NUMBER")
        elif ctx.STRING():
            combined = ''.join(eval(s.getText()) for s in ctx.STRING())
            atom_node = Constant(node_type=NodeType.CONSTANT, value=combined, dtype="STRING")
        return atom_node

    # Binary operations - assuming your grammar has this rule or something similar
    def visitExpr(self, ctx: PythonParser.ExprContext) -> Expression:
        # Simplify: if expr has two children with operator in middle => binary op
        children = list(ctx.getChildren())
        if len(children) == 3:
            left = self.visit(ctx.getChild(0))
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.getChild(2))
            return BinaryOp(node_type=NodeType.BINARY_OP, left=left, operator=operator, right=right)
        elif ctx.trailer():
            for tr in ctx.trailer():
                if tr.arguments():
                    args = [self.visit(arg) for arg in tr.arguments().arglist().argument()]
                    return Call(node_type=NodeType.CALL, identifier=self.visit(ctx.atom()), args=args)
        else:
            return self.visit(ctx.getChild(0))

    # Name nodes
    def visitName(self, ctx: PythonParser.NameContext) -> Name:
        return Name(node_type=NodeType.NAME, id=ctx.getText(), ctx='Load')

    # Constants (numbers, strings)
    def visitNumber(self, ctx: PythonParser.NumberContext) -> Constant:
        val = eval(ctx.getText())
        return Constant(node_type=NodeType.CONSTANT, value=val)

    # More visit methods for other node types go here...
    
    # Fallback
    def visitChildren(self, node):
        if not node:
            return None
        results = []
        for c in node.getChildren():
            res = self.visit(c)
            if res:
                results.append(res)
        if len(results) == 1:
            return results[0]
        return results

