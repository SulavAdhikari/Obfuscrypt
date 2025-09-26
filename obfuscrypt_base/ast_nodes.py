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
    IF = "If"
    WHILE = "While"
    FOR = "For"
    TRY = "Try"
    WITH = "With"
    RAISE = "Raise"
    IMPORT = "Import"
    IMPORT_FROM = "ImportFrom"
    
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
    location: Optional[Location] = None
    
    def __init__(self, node_type: NodeType, location: Optional[Location] = None):
        self.node_type = node_type
        self.location = location
    
    def to_dict(self) -> dict:
        result = {"type": self.node_type.value}
        if self.location:
            result["location"] = {
                "start": {"line": self.location.start.line, "column": self.location.start.column},
                "end": {"line": self.location.end.line, "column": self.location.end.column}
            }
        return result

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

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
class Arg:
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
class IfStmt(Statement):
    node_type: NodeType = NodeType.IF
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


