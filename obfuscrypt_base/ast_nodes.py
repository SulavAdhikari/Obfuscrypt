from typing import List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum

class NodeType(Enum):
    # Statements
    MODULE = "Module"
    FUNCTION_DEF = "FunctionDef"
    CLASS_DEF = "ClassDef"
    RETURN = "Return"
    ASSIGN = "Assign"
    IF = "IfStatement"
    ELSE = "ElseStatement"
    ELIF = "ElifStatement"
    WHILE = "WhileStatement"
    FOR = "ForStatement"
    TRY = "TryStatement"
    WITH = "With"
    RAISE = "Raise"
    IMPORT = "Import"
    IMPORT_FROM = "ImportFrom"
    PASS = "Pass"
    BREAK = "Break"
    CONTINUE = "Continue"

    # Expressions
    BINARY_OP = "BinaryOp"
    UNARY_OP = "UnaryOp"
    CALL = "Call"
    ATTRIBUTE = "Attribute"
    SUBSCRIPT = "Subscript"
    NAME = "Name"
    CONSTANT = "Constant"
    LIST = "List"
    TUPLE = "Tuple"
    DICT = "Dict"
    SET = "Set"
    LAMBDA = "Lambda"
    
    # Others
    ARGUMENTS = "Arguments"
    KEYWORD = "Keyword"
    DECORATOR = "Decorator"



@dataclass
class Position:
    line: int
    column: int
    
@dataclass
class Location:
    start: Position
    end: Position

class ASTNode:
    def __init__(self, node_type: NodeType):
        self.node_type = node_type
    
    @classmethod
    def from_dict(cls, json_data: dict):
        """
        Reconstructs the AST node from a dictionary
        """
        if not json_data:
            return None
        
        node_type_str = json_data.get("type")
        if not node_type_str:
            if "args" in json_data and isinstance(json_data["args"], list):
                node_type_str = NodeType.ARGUMENTS.value
            elif "name" in json_data and "asname" in json_data:
                node = Alias()
                node.name = json_data.get("name", "")
                node.asname = json_data.get("asname")
                return node
            elif "name" in json_data and "annotation" in json_data:
                node = Arg(name=json_data.get("name", ""))
                node.annotation = cls.from_dict(json_data.get("annotation")) if json_data.get("annotation") else None
                return node
            elif "arg" in json_data and "value" in json_data:
                node = ASTNode(NodeType.KEYWORD)
                node.arg = json_data.get("arg", "")
                node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
                return node
            else:
                return json_data

        if node_type_str == NodeType.MODULE.value:
            node = Module(NodeType.MODULE, body=[])
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            return node
            
        elif node_type_str == NodeType.FUNCTION_DEF.value:
            node = FunctionDef(NodeType.FUNCTION_DEF, name=json_data.get("name", ""), 
                               args=Arguments(NodeType.ARGUMENTS, args=[], vararg=None, kwarg=None, defaults=[]), 
                               body=[], decorator_list=[], returns=None)
            node.args = cls.from_dict(json_data.get("args", {}))
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.decorator_list = [cls.from_dict(dec) for dec in json_data.get("decorator_list", [])]
            node.returns = cls.from_dict(json_data.get("returns")) if json_data.get("returns") else None
            node.async_ = json_data.get("async", False)
            return node
            
        elif node_type_str == NodeType.CLASS_DEF.value:
            node = ASTNode(NodeType.CLASS_DEF)
            node.name = json_data.get("name", "")
            node.bases = [cls.from_dict(base) for base in json_data.get("bases", [])]
            node.keywords = [cls.from_dict(kw) for kw in json_data.get("keywords", [])]
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.decorator_list = [cls.from_dict(dec) for dec in json_data.get("decorator_list", [])]
            return node
            
        elif node_type_str == NodeType.RETURN.value:
            node = ReturnStmt(NodeType.RETURN)
            node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            return node
            
        elif node_type_str == NodeType.ASSIGN.value:
            node = Assign(NodeType.ASSIGN)
            node.targets = [cls.from_dict(target) for target in json_data.get("targets", [])]
            node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            node.operator = json_data.get("operator", "=")
            return node
            
        elif node_type_str == NodeType.IF.value:
            node = IfStmt(NodeType.IF)
            node.test = cls.from_dict(json_data.get("test")) if json_data.get("test") else None
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.elif_clauses = [cls.from_dict(e) for e in json_data.get("ifelse", [])] if json_data.get("ifelse") else []
            node.else_clause = cls.from_dict(json_data.get("else")) if json_data.get("else") else None
            return node
            
        elif node_type_str == NodeType.ELIF.value:
            node = ElifStmt(NodeType.ELIF)
            node.test = cls.from_dict(json_data.get("test")) if json_data.get("test") else None
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            return node
            
        elif node_type_str == NodeType.ELSE.value:
            node = ElseStmt(NodeType.ELSE)
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            return node
            
        elif node_type_str == NodeType.WHILE.value:
            node = WhileStmt(NodeType.WHILE)
            node.test = cls.from_dict(json_data.get("test")) if json_data.get("test") else None
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.orelse = [cls.from_dict(stmt) for stmt in json_data.get("orelse", [])]
            return node
            
        elif node_type_str == NodeType.FOR.value:
            node = ForStmt(NodeType.FOR)
            node.target = cls.from_dict(json_data.get("target")) if json_data.get("target") else None
            node.iter = cls.from_dict(json_data.get("iter")) if json_data.get("iter") else None
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.orelse = [cls.from_dict(stmt) for stmt in json_data.get("orelse", [])]
            node.async_ = json_data.get("async", False)
            return node
            
        elif node_type_str == NodeType.TRY.value:
            node = ASTNode(NodeType.TRY)
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            node.handlers = [cls.from_dict(h) for h in json_data.get("handlers", [])]
            node.orelse = [cls.from_dict(stmt) for stmt in json_data.get("orelse", [])]
            node.finalbody = [cls.from_dict(stmt) for stmt in json_data.get("finalbody", [])]
            return node
            
        elif node_type_str == NodeType.WITH.value:
            node = ASTNode(NodeType.WITH)
            node.items = [cls.from_dict(item) for item in json_data.get("items", [])]
            node.body = [cls.from_dict(stmt) for stmt in json_data.get("body", [])]
            return node
            
        elif node_type_str == NodeType.RAISE.value:
            node = RaiseStmt(NodeType.RAISE)
            node.exc = cls.from_dict(json_data.get("exc")) if json_data.get("exc") else None
            node.cause = cls.from_dict(json_data.get("cause")) if json_data.get("cause") else None
            return node
            
        elif node_type_str == NodeType.IMPORT.value:
            node = ImportStmt(NodeType.IMPORT)
            node.names = [cls.from_dict(n) for n in json_data.get("names", [])]
            return node
            
        elif node_type_str == NodeType.IMPORT_FROM.value:
            node = ImportFromStmt(NodeType.IMPORT_FROM)
            node.module = json_data.get("module")
            node.names = [cls.from_dict(n) for n in json_data.get("names", [])]
            node.level = json_data.get("level")
            return node
            
        elif node_type_str == NodeType.PASS.value:
            return PassStmt(NodeType.PASS)
            
        elif node_type_str == NodeType.BREAK.value:
            return BreakStmt(NodeType.BREAK)
            
        elif node_type_str == NodeType.CONTINUE.value:
            return ContinueStmt(NodeType.CONTINUE)
            
        elif node_type_str == NodeType.BINARY_OP.value:
            left = cls.from_dict(json_data.get("left")) if json_data.get("left") else None
            right = cls.from_dict(json_data.get("right")) if json_data.get("right") else None
            operator_val = json_data.get("operator") or json_data.get("op", "")
            return BinaryOp(NodeType.BINARY_OP, left=left, operator=operator_val, right=right)
            
        elif node_type_str == NodeType.UNARY_OP.value:
            op_val = json_data.get("operator") or json_data.get("op", "")
            operand = cls.from_dict(json_data.get("operand")) if json_data.get("operand") else None
            return UnaryOp(NodeType.UNARY_OP, operator=op_val, operand=operand)
            
        elif node_type_str == NodeType.CALL.value:
            identifier = cls.from_dict(json_data.get("identifier")) or cls.from_dict(json_data.get("func"))
            args_list = [cls.from_dict(arg) for arg in json_data.get("args", [])]
            node = Call(NodeType.CALL, identifier=identifier, args=args_list)
            if "keywords" in json_data:
                node.keywords = [cls.from_dict(kw) for kw in json_data.get("keywords", [])]
            return node
            
        elif node_type_str == NodeType.ATTRIBUTE.value:
            node = Attribute(NodeType.ATTRIBUTE)
            node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            node.attr = json_data.get("attr", "")
            return node
            
        elif node_type_str == NodeType.SUBSCRIPT.value:
            node = Subscript(NodeType.SUBSCRIPT)
            node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            node.slice = cls.from_dict(json_data.get("slice")) if json_data.get("slice") else None
            return node
            
        elif node_type_str == NodeType.NAME.value:
            node = Name(NodeType.NAME, id=json_data.get("id", ""), ctx=json_data.get("ctx", ""))
            return node
            
        elif node_type_str == NodeType.CONSTANT.value:
            node = Constant(NodeType.CONSTANT, value=json_data.get("value"), dtype=json_data.get("dtype"))
            return node
            
        elif node_type_str == NodeType.LIST.value:
            node = ListExpr(NodeType.LIST)
            node.elts = [cls.from_dict(elt) for elt in json_data.get("elts", [])]
            return node
            
        elif node_type_str == NodeType.TUPLE.value:
            node = TupleExpr(NodeType.TUPLE)
            node.elts = [cls.from_dict(elt) for elt in json_data.get("elts", [])]
            return node
            
        elif node_type_str == NodeType.DICT.value:
            node = DictExpr(NodeType.DICT)
            node.keys = [cls.from_dict(k) if k else None for k in json_data.get("keys", [])]
            node.values = [cls.from_dict(v) for v in json_data.get("values", [])]
            return node
            
        elif node_type_str == NodeType.SET.value:
            node = SetExpr(NodeType.SET)
            node.elts = [cls.from_dict(elt) for elt in json_data.get("elts", [])]
            return node
            
        elif node_type_str == NodeType.LAMBDA.value:
            node = ASTNode(NodeType.LAMBDA)
            node.args = cls.from_dict(json_data.get("args")) if json_data.get("args") else None
            node.body = cls.from_dict(json_data.get("body")) if json_data.get("body") else None
            return node
            
        elif node_type_str == NodeType.ARGUMENTS.value:
            args_list = [cls.from_dict(arg) for arg in json_data.get("args", [])]
            vararg = cls.from_dict(json_data.get("vararg")) if json_data.get("vararg") else None
            kwarg = cls.from_dict(json_data.get("kwarg")) if json_data.get("kwarg") else None
            defaults = [cls.from_dict(d) for d in json_data.get("defaults", [])]
            node = Arguments(NodeType.ARGUMENTS, args=args_list, vararg=vararg, kwarg=kwarg, defaults=defaults)
            return node
            
        elif node_type_str == NodeType.KEYWORD.value:
            node = ASTNode(NodeType.KEYWORD)
            node.arg = json_data.get("arg", "")
            node.value = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            return node
            
        elif node_type_str == NodeType.DECORATOR.value:
            node = Decorator(NodeType.DECORATOR)
            node.expression = cls.from_dict(json_data.get("value")) if json_data.get("value") else None
            return node
            
        return None

    # Every node should implement this method
    def to_dict(self) -> dict:
        return {"type": self.node_type.value}

        
    

    # Gets ASTObject instance of the node for analysis and transformation
    def get_object(self):
        from obfuscrypt_base.ast_object import ASTObject
        return ASTObject(self)
    
    def get_from_json(self, json_data: dict):
        """
        Reconstructs the AST node from a dictionary
        """
        self.node_type = self.get_node_type_from_string(json_data["type"])
    
        
        

class Statement(ASTNode):
    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
        self.is_statement_node = True



class Expression(ASTNode):
    def __init__(self, node_type: NodeType):
        super().__init__(node_type)
        self.is_expression_node = True



@dataclass
class Module(Statement):
    node_type: NodeType
    body: List[Statement]
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result["body"] = [stmt.to_dict() for stmt in self.body]
        return result

    

@dataclass
class FunctionDef(Statement):
    node_type: NodeType
    name: str
    args: 'Arguments'
    body: List[Statement]
    decorator_list: List['Decorator']
    returns: Optional[Expression]
    async_: bool = False
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "name": self.name,
            "args": self.args.to_dict(),
            "body": [stmt.to_dict() for stmt in self.body],
            "decorator_list": [dec.to_dict() for dec in self.decorator_list],
            "returns": self.returns.to_dict() if self.returns else None,
            "async": self.async_
        })
        return result

@dataclass
class Arguments:
    node_type: NodeType
    args: List['Arg']
    vararg: Optional['Arg']
    kwarg: Optional['Arg']
    defaults: List[Expression]
    
    def to_dict(self) -> dict:
        return {
            "args": [arg.to_dict() for arg in self.args],
            "vararg": self.vararg.to_dict() if self.vararg else None,
            "kwarg": self.kwarg.to_dict() if self.kwarg else None,
            "defaults": [default.to_dict() for default in self.defaults]
        }

@dataclass
class Arg(Expression):
    name: str
    annotation: Optional[Expression] = None
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "annotation": self.annotation.to_dict() if self.annotation else None
        }

@dataclass
class BinaryOp(Expression):
    node_type: NodeType
    left: Expression
    operator: str
    right: Expression
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "left": self.left.to_dict(),
            "operator": self.operator,
            "right": self.right.to_dict()
        })
        return result

@dataclass
class UnaryOp(Expression):
    node_type: NodeType
    operator: str
    operand: Expression
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "operator": self.operator,
            "operand": self.operand.to_dict()
        })
        return result

@dataclass
class Call(Expression):
    node_type: NodeType
    identifier: Expression
    args: List[Expression]
    # keywords: List[Keyword]
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "identifier": self.identifier.to_dict(),
            "args": [arg.to_dict() for arg in self.args],
            #"keywords": [kw.to_dict() for kw in self.keywords]
        })
        return result

@dataclass
class Constant(Expression):
    node_type: NodeType
    value: Any
    dtype: Optional[str] = None
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "value": self.value,
            "dtype": self.dtype
        })
        return result

@dataclass
class Name(Expression):
    node_type: NodeType
    id: str
    ctx: str  # 'Load', 'Store', or 'Del'
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "id": self.id,
            "ctx": self.ctx
        })
        return result

# Add more node types as needed based on the grammar

@dataclass
class Assign(Statement):
    node_type: NodeType = NodeType.ASSIGN
    targets: List[Expression] = field(default_factory=list)  # You had list[str] but targets can be any expression (Name, Attribute, Subscript)
    value: Expression = None
    operator: str = "="

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "targets": [target.to_dict() for target in self.targets],
            "operator": self.operator if self.operator else None,
            "value": self.value.to_dict() if self.value else None
        })
        return result


@dataclass
class Decorator(ASTNode):
    node_type: NodeType = NodeType.DECORATOR
    expression: Expression = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["expression"] = self.expression.to_dict() if self.expression else None
        return result


@dataclass
class Attribute(Expression):
    node_type: NodeType = NodeType.ATTRIBUTE
    value: Expression = None
    attr: str = ""

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "value": self.value.to_dict() if self.value else None,
            "attr": self.attr
        })
        return result


@dataclass
class Subscript(Expression):
    node_type: NodeType = NodeType.SUBSCRIPT
    value: Expression = None
    slice: Expression = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "value": self.value.to_dict() if self.value else None,
            "slice": self.slice.to_dict() if self.slice else None
        })
        return result


@dataclass
class ListExpr(Expression):
    node_type: NodeType = NodeType.LIST
    elts: List[Expression] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["elts"] = [elt.to_dict() for elt in self.elts]
        return result


@dataclass
class TupleExpr(Expression):
    node_type: NodeType = NodeType.TUPLE
    elts: List[Expression] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["elts"] = [elt.to_dict() for elt in self.elts]
        return result


@dataclass
class DictExpr(Expression):
    node_type: NodeType = NodeType.DICT
    keys: List[Optional[Expression]] = field(default_factory=list)
    values: List[Expression] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "keys": [key.to_dict() if key else None for key in self.keys],
            "values": [value.to_dict() for value in self.values]
        })
        return result


@dataclass
class SetExpr(Expression):
    node_type: NodeType = NodeType.SET
    elts: List[Expression] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["elts"] = [elt.to_dict() for elt in self.elts]
        return result

@dataclass
class ElifStmt(Statement):
    node_type: NodeType = NodeType.ELIF
    test: Expression = None
    body: List[Statement] = field(default_factory=list)


    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "test": self.test.to_dict() if self.test else None,
            "body": [stmt.to_dict() for stmt in self.body],
        })
        return result

@dataclass
class ElseStmt(Statement):
    node_type: NodeType = NodeType.ELSE
    body: List[Statement] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "body": [stmt.to_dict() for stmt in self.body],
        })
        return result

@dataclass
class IfStmt(Statement):
    node_type: NodeType = NodeType.IF
    test: Expression = None
    body: List[Statement] = field(default_factory=list)
    elif_clauses: ElifStmt = field(default_factory=list)
    else_clause: ElseStmt = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "test": self.test.to_dict() if self.test else None,
            "body": [stmt.to_dict() for stmt in self.body],
            "ifelse": [e.to_dict() for e in self.elif_clauses] if self.elif_clauses else None,
            "else": self.else_clause.to_dict() if self.else_clause else None
        })
        return result


@dataclass
class WhileStmt(Statement):
    node_type: NodeType = NodeType.WHILE
    test: Expression = None
    body: List[Statement] = field(default_factory=list)
    orelse: List[Statement] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "test": self.test.to_dict() if self.test else None,
            "body": [stmt.to_dict() for stmt in self.body],
            "orelse": [stmt.to_dict() for stmt in self.orelse]
        })
        return result


@dataclass
class ForStmt(Statement):
    node_type: NodeType = NodeType.FOR
    target: Expression = None
    iter: Expression = None
    body: List[Statement] = field(default_factory=list)
    orelse: List[Statement] = field(default_factory=list)
    async_: bool = False

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "target": self.target.to_dict() if self.target else None,
            "iter": self.iter.to_dict() if self.iter else None,
            "body": [stmt.to_dict() for stmt in self.body],
            "orelse": [stmt.to_dict() for stmt in self.orelse],
            "async": self.async_
        })
        return result


@dataclass
class ReturnStmt(Statement):
    node_type: NodeType = NodeType.RETURN
    value: Optional[Expression] = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        if self.value:
            if type(self.value) == list:
                result["value"] = []
                for val in self.value:
                    result["value"].append(val.to_dict())
            else:
                result["value"] = self.value.to_dict()
        else:
            result["value"] = None
        return result


@dataclass
class RaiseStmt(Statement):
    node_type: NodeType = NodeType.RAISE
    exc: Optional[Expression] = None
    cause: Optional[Expression] = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "exc": self.exc.to_dict() if self.exc else None,
            "cause": self.cause.to_dict() if self.cause else None
        })
        return result


@dataclass
class ImportStmt(Statement):
    node_type: NodeType = NodeType.IMPORT
    names: List['Alias'] = field(default_factory=list)

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["names"] = [alias.to_dict() for alias in self.names]
        return result


@dataclass
class ImportFromStmt(Statement):
    node_type: NodeType = NodeType.IMPORT_FROM
    module: Optional[str] = None
    names: List['Alias'] = field(default_factory=list)
    level: Optional[int] = None

    def to_dict(self) -> dict:
        result = super().to_dict()
        result.update({
            "module": self.module,
            "names": [alias.to_dict() for alias in self.names],
            "level": self.level
        })
        return result


@dataclass
class Alias(ASTNode):
    name: str = ""
    asname: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "asname": self.asname
        }


@dataclass
class PassStmt(Statement):
    node_type: NodeType = NodeType.PASS

    def to_dict(self) -> dict:
        return super().to_dict()


@dataclass
class BreakStmt(Statement):
    node_type: NodeType = NodeType.BREAK

    def to_dict(self) -> dict:
        return super().to_dict()


@dataclass
class ContinueStmt(Statement):
    node_type: NodeType = NodeType.CONTINUE

    def to_dict(self) -> dict:
        return super().to_dict()
