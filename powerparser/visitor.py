from obfuscrypt.obfuscrypt_base import Structure, print_structure
from powerparser.PowerExpVisitor import PowerExpVisitor

class Visitor(PowerExpVisitor):
    
    def visit(self, tree):
        try:
            return super().visit(tree)
        except Exception as e:
            print("error ", e)
            return ""

    def visitScript(self, ctx):
        parameters = []
        for children in ctx.getChildren():
            if children.getText() == "<EOF>":
                parameters.append('')
                break
            else:
                parameters.append(self.visit(children))
        return Structure(class_type="CodeBlock", parameters=parameters)
    
    def visitIdentifier(self, ctx):
        query = ctx.getText()
        query = self.change_column_query(query)
        return Structure('Identifier', value=query)

    def visitFunctionCall(self, ctx):
        children = list(ctx.getChildren())
        fun_name = children[0].getText().upper()
        parameters = []
        for child in children[2:-1]:
            if child.getText() == ',':
                continue
            param = self.visit(child)
            parameters.append(param)
        return Structure(class_type='Function', function_name=fun_name, parameters=parameters)
    
    def visitCommandStatement(self, ctx):
        children = list(ctx.getChildren())
        # handling for arguments passed is not done i.e. --arg val
        parameters = []
        for child in children:
            if child.getText() == ',':
                continue
            param = self.visit(child)
            parameters.append(param)
        return Structure(class_type='Operation', value="CommandExecution", parameters=parameters)

    def visitCodeBlock(self, ctx):
        parameters = []
        for children in ctx.getChildren():
            if children.getText() == "<EOF>":
                parameters.append('')
                break
            else:
                parameters.append(self.visit(children))
        return Structure(class_type="CodeBlock", parameters=parameters)
    
    def visitFunctionDecl(self, ctx):
        children = list(ctx.getChildren())
        parameters = []
        for child in children:
            if child.getText() in ['function', '{', '}']:
                continue
            param = self.visit(child)
            parameters.append(param)
        return Structure(class_type='Operation', value="FunctionDefinition", parameters=parameters)

    def visitFunctionCall(self, ctx):
        children = list(ctx.getChildren())
        fun_name = children[0]
        parameters = []
        for child in children[1:]:
            if child.getText() ==',':
                continue
            param = self.visit(child)
            parameters.append(param)
        return Structure(class_type='Function', function_name=fun_name, parameters=parameters)
