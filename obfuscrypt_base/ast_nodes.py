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

    statement_nodes = [MODULE, FUNCTION_DEF, CLASS_DEF, RETURN, ASSIGN, IF, ELSE, ELIF, WHILE, FOR, TRY, WITH, RAISE, IMPORT, IMPORT_FROM, PASS, BREAK, CONTINUE]
    expression_nodes = [BINARY_OP, UNARY_OP, CALL, ATTRIBUTE, SUBSCRIPT, NAME, CONSTANT, LIST, TUPLE, DICT, SET, LAMBDA]


    def get_node_class_from_string(self, node_type: str):
        note_type_to_class_map = {
            "Module": Module(NodeType.MODULE),
            "FunctionDef": FunctionDef(NodeType.FUNCTION_DEF),
            "ClassDef": ClassDef(NodeType.CLASS_DEF),
            "Return": Return(NodeType.RETURN),
            "Assign": Assign(NodeType.ASSIGN),
            "If": IfStmt(NodeType.IF),
            "Else": ElseStmt(NodeType.ELSE),
            "Elif": ElifStmt(NodeType.ELIF),
            "While": WhileStmt(NodeType.WHILE),
            "For": ForStmt(NodeType.FOR),
            "Try": TryStmt(NodeType.TRY),
            "With": WithStmt(NodeType.WITH),
            "Raise": RaiseStmt(NodeType.RAISE),
            "Import": ImportStmt(NodeType.IMPORT),
            "ImportFrom": ImportFromStmt(NodeType.IMPORT_FROM),
            "Pass": PassStmt(NodeType.PASS),
            "Break": BreakStmt(NodeType.BREAK),
            "Continue": ContinueStmt(NodeType.CONTINUE),
            "BinaryOp": BinaryOp(NodeType.BINARY_OP),
            "UnaryOp": UnaryOp(NodeType.UNARY_OP),
            "Call": Call(NodeType.CALL),
            "Attribute": Attribute(NodeType.ATTRIBUTE),
            "Subscript": Subscript(NodeType.SUBSCRIPT),
            "Name": Name(NodeType.NAME),
            "Constant": Constant(NodeType.CONSTANT),
            "List": List(NodeType.LIST),
            "Tuple": Tuple(NodeType.TUPLE),
            "Dict": Dict(NodeType.DICT),
            "Set": Set(NodeType.SET),
            "Lambda": Lambda(NodeType.LAMBDA),
            "Arguments": Arguments(NodeType.ARGUMENTS),
            "Keyword": Keyword(NodeType.KEYWORD),
            "Decorator": Decorator(NodeType.DECORATOR),
        }

        if node_type in note_type_to_class_map:
            return note_type_to_class_map[node_type]
        else:
            raise ValueError(f"Unknown node type: {node_type}")


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
        node = NodeType.get_node_from_string(json_data["type"])
        if json_data["Type"] == "Module":
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
        elif json_data["Type"] == "FunctionDef":
            node.name = json_data["name"]
            node.args = ASTNode.from_dict(json_data["args"])
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.decorator_list = [ASTNode.from_dict(dec) for dec in json_data["decorator_list"]]
            node.returns = ASTNode.from_dict(json_data["returns"])
            node.async_ = json_data["async"]
        elif json_data["Type"] == "ClassDef":
            node.name = json_data["name"]
            node.bases = [ASTNode.from_dict(base) for base in json_data["bases"]]
            node.keywords = [ASTNode.from_dict(keyword) for keyword in json_data["keywords"]]
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.decorator_list = [ASTNode.from_dict(dec) for dec in json_data["decorator_list"]]
        elif json_data["Type"] == "Return":
            node.value = ASTNode.from_dict(json_data["value"])
        elif json_data["Type"] == "Assign":
            node.targets = [ASTNode.from_dict(target) for target in json_data["targets"]]
            node.value = ASTNode.from_dict(json_data["value"])
        elif json_data["Type"] == "If":
            node.test = ASTNode.from_dict(json_data["test"])
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.orelse = [ASTNode.from_dict(stmt) for stmt in json_data["orelse"]]
        elif json_data["Type"] == "While":
            node.test = ASTNode.from_dict(json_data["test"])
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.orelse = [ASTNode.from_dict(stmt) for stmt in json_data["orelse"]]
        elif json_data["Type"] == "For":
            node.target = ASTNode.from_dict(json_data["target"])
            node.iter = ASTNode.from_dict(json_data["iter"])
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.orelse = [ASTNode.from_dict(stmt) for stmt in json_data["orelse"]]
        elif json_data["Type"] == "Try":
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
            node.handlers = [ASTNode.from_dict(handler) for handler in json_data["handlers"]]
            node.orelse = [ASTNode.from_dict(stmt) for stmt in json_data["orelse"]]
            node.finalbody = [ASTNode.from_dict(stmt) for stmt in json_data["finalbody"]]
        elif json_data["Type"] == "With":
            node.items = [ASTNode.from_dict(item) for item in json_data["items"]]
            node.body = [ASTNode.from_dict(stmt) for stmt in json_data["body"]]
        elif json_data["Type"] == "Raise":
            node.exc = ASTNode.from_dict(json_data["exc"])
            node.cause = ASTNode.from_dict(json_data["cause"])
        elif json_data["Type"] == "Import":
            node.names = [ASTNode.from_dict(name) for name in json_data["names"]]
        elif json_data["Type"] == "ImportFrom":
            node.module = json_data["module"]
            node.names = [ASTNode.from_dict(name) for name in json_data["names"]]
            node.level = json_data["level"]
        elif json_data["Type"] == "Pass":
            pass
        elif json_data["Type"] == "Break":
            pass
        elif json_data["Type"] == "Continue":
            pass
        elif json_data["Type"] == "BinaryOp":
            node.left = ASTNode.from_dict(json_data["left"])
            node.op = ASTNode.from_dict(json_data["op"])
            node.right = ASTNode.from_dict(json_data["right"])
        elif json_data["Type"] == "UnaryOp":
            node.op = ASTNode.from_dict(json_data["op"])
            node.operand = ASTNode.from_dict(json_data["operand"])
        elif json_data["Type"] == "Call":
            node.func = ASTNode.from_dict(json_data["func"])
            node.args = [ASTNode.from_dict(arg) for arg in json_data["args"]]
            node.keywords = [ASTNode.from_dict(keyword) for keyword in json_data["keywords"]]
        elif json_data["Type"] == "Attribute":
            node.value = ASTNode.from_dict(json_data["value"])
            node.attr = json_data["attr"]
        elif json_data["Type"] == "Subscript":
            node.value = ASTNode.from_dict(json_data["value"])
            node.slice = ASTNode.from_dict(json_data["slice"])
        elif json_data["Type"] == "Name":
            node.id = json_data["id"]
            node.ctx = ASTNode.from_dict(json_data["ctx"])
        elif json_data["Type"] == "Constant":
            node.value = json_data["value"]
        elif json_data["Type"] == "List":
            node.elts = [ASTNode.from_dict(elt) for elt in json_data["elts"]]
        elif json_data["Type"] == "Tuple":
            node.elts = [ASTNode.from_dict(elt) for elt in json_data["elts"]]
        elif json_data["Type"] == "Dict":
            node.keys = [ASTNode.from_dict(key) for key in json_data["keys"]]
            node.values = [ASTNode.from_dict(value) for value in json_data["values"]]
        elif json_data["Type"] == "Set":
            node.elts = [ASTNode.from_dict(elt) for elt in json_data["elts"]]
        elif json_data["Type"] == "Lambda":
            node.args = ASTNode.from_dict(json_data["args"])
            node.body = ASTNode.from_dict(json_data["body"])
        elif json_data["Type"] == "Arguments":
            node.args = [ASTNode.from_dict(arg) for arg in json_data["args"]]
            node.vararg = ASTNode.from_dict(json_data["vararg"])
            node.kwarg = ASTNode.from_dict(json_data["kwarg"])
            node.defaults = [ASTNode.from_dict(default) for default in json_data["defaults"]]
        elif json_data["Type"] == "Keyword":
            node.arg = json_data["arg"]
            node.value = ASTNode.from_dict(json_data["value"])
        elif json_data["Type"] == "Decorator":
            node.value = ASTNode.from_dict(json_data["value"])  
        return node

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
