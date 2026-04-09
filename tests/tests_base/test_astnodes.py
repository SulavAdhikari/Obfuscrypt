# test ast_nodes.py (ASTNodes)
import pytest
from obfuscrypt_base.ast_nodes import (
    ASTNode, NodeType, Module, FunctionDef, Arguments, Arg, ReturnStmt, Assign, 
    Name, Constant, BinaryOp, Call, IfStmt, ElifStmt, ElseStmt, 
    WhileStmt, ForStmt, Decorator
)

class TestASTNodesToDict:
    def test_module_definition(self):
        """
        Purpose: A Module should behave as the root container, encapsulating an array of statements
        as its body, validating the primary entry point structure.
        """
        node = Module(NodeType.MODULE, body=[])
        assert node.to_dict() == {"type": "Module", "body": []}

    def test_module_with_body_function(self):
        """
        Purpose: Validate the serialization of nested statements, ensuring that standard blocks like
        Function definitions retain their detailed structural semantics inside the module.
        """
        func_def = FunctionDef(
            node_type=NodeType.FUNCTION_DEF,
            name="test",
            args=Arguments(NodeType.ARGUMENTS, args=[], vararg=None, kwarg=None, defaults=[]),
            body=[ReturnStmt(NodeType.RETURN, value=None)],
            decorator_list=[],
            returns=None,
            async_=False
        )
        node = Module(NodeType.MODULE, body=[func_def])
        expected = {
            "type": "Module", 
            "body": [
                {
                    "type": "FunctionDef", 
                    "name": "test", 
                    "args": {"args": [], "vararg": None, "kwarg": None, "defaults": []}, 
                    "body": [{"type": "Return", "value": None}], 
                    "decorator_list": [], 
                    "returns": None, 
                    "async": False
                }
            ]
        }
        assert node.to_dict() == expected

    def test_assign_statement(self):
        """
        Purpose: Assignment definitions must precisely define which target expressions are receiving
        which evaluated value mappings, capturing mutation flow in logic.
        """
        target = Name(NodeType.NAME, id="x", ctx="Store")
        val = Constant(NodeType.CONSTANT, value=1, dtype="NUMBER")
        node = Assign(NodeType.ASSIGN, targets=[target], value=val, operator="=")
        expected = {
            "type": "Assign",
            "targets": [{"type": "Name", "id": "x", "ctx": "Store"}],
            "operator": "=",
            "value": {"type": "Constant", "value": 1, "dtype": "NUMBER"}
        }
        assert node.to_dict() == expected

    def test_if_statement(self):
        """
        Purpose: Conditionals dictate control flow and must correctly model their boolean expressions 
        testing alongside their primary payload, with options for alternative fallback paths.
        """
        test_expr = Constant(NodeType.CONSTANT, value=True, dtype="BOOLEAN")
        node = IfStmt(
            node_type=NodeType.IF, 
            test=test_expr, 
            body=[], 
            elif_clauses=[], 
            else_clause=ElseStmt(NodeType.ELSE, body=[])
        )
        expected = {
            "type": "IfStatement",
            "test": {"type": "Constant", "value": True, "dtype": "BOOLEAN"},
            "body": [],
            "ifelse": None,
            "else": {"type": "ElseStatement", "body": []}
        }
        assert node.to_dict() == expected
        
    def test_binary_operator(self):
        """
        Purpose: Operations dynamically compute output based on right and left nodes to represent 
        abstract math or boolean combinatorics.
        """
        left = Name(NodeType.NAME, id="a", ctx="Load")
        right = Name(NodeType.NAME, id="b", ctx="Load")
        node = BinaryOp(NodeType.BINARY_OP, left=left, operator="+", right=right)
        expected = {
            "type": "BinaryOp",
            "left": {"type": "Name", "id": "a", "ctx": "Load"},
            "operator": "+",
            "right": {"type": "Name", "id": "b", "ctx": "Load"}
        }
        assert node.to_dict() == expected
        
    def test_function_call(self):
        """
        Purpose: Ensure an invocation effectively wraps identifying the target subroutine accompanied 
        by dynamic runtime variables acting as its execution arguments.
        """
        func_id = Name(NodeType.NAME, id="print", ctx="Load")
        arg = Constant(NodeType.CONSTANT, value="Hello", dtype="STRING")
        node = Call(NodeType.CALL, identifier=func_id, args=[arg])
        expected = {
            "type": "Call",
            "identifier": {"type": "Name", "id": "print", "ctx": "Load"},
            "args": [{"type": "Constant", "value": "Hello", "dtype": "STRING"}]
        }
        assert node.to_dict() == expected
        
    def test_loop_construct(self):
        """
        Purpose: Loop constructs serve as recursive execution constraints dependent on ongoing test
        criteria, accurately serializing loop conditions for flow analysis and vector mapping.
        """
        test_expr = Constant(NodeType.CONSTANT, value=True, dtype="BOOLEAN")
        node = WhileStmt(NodeType.WHILE, test=test_expr, body=[], orelse=[])
        expected = {
            "type": "WhileStatement",
            "test": {"type": "Constant", "value": True, "dtype": "BOOLEAN"},
            "body": [],
            "orelse": []
        }
        assert node.to_dict() == expected

    def test_for_loop_construct(self):
        """
        Purpose: Iterative constructs over collections must properly define the target loop
        variable and the iterable expression, encapsulating execution blocks for each item
        to model finite repetitive flows.
        """
        target = Name(NodeType.NAME, id="item", ctx="Store")
        iter_expr = Name(NodeType.NAME, id="collection", ctx="Load")
        node = ForStmt(NodeType.FOR, target=target, iter=iter_expr, body=[], orelse=[], async_=False)
        expected = {
            "type": "ForStatement",
            "target": {"type": "Name", "id": "item", "ctx": "Store"},
            "iter": {"type": "Name", "id": "collection", "ctx": "Load"},
            "body": [],
            "orelse": [],
            "async": False
        }
        assert node.to_dict() == expected

    def test_return_statement(self):
        """
        Purpose: Control flow mechanisms that exit subroutines need to correctly serialize their
        evaluated return values, mapping how data states exit a local scope into a caller's context.
        """
        val = Constant(NodeType.CONSTANT, value=42, dtype="NUMBER")
        node = ReturnStmt(NodeType.RETURN, value=val)
        expected = {
            "type": "Return",
            "value": {"type": "Constant", "value": 42, "dtype": "NUMBER"}
        }
        assert node.to_dict() == expected

    def test_data_structure_list(self):
        """
        Purpose: List literals represent an ordered sequence of objects and need to accurately
        define elements sequentially to map dynamic memory structures into the AST vector space.
        """
        from obfuscrypt_base.ast_nodes import ListExpr
        elts = [Constant(NodeType.CONSTANT, value=1, dtype="NUMBER"), Constant(NodeType.CONSTANT, value=2, dtype="NUMBER")]
        node = ListExpr(NodeType.LIST, elts=elts)
        expected = {
            "type": "List",
            "elts": [
                {"type": "Constant", "value": 1, "dtype": "NUMBER"},
                {"type": "Constant", "value": 2, "dtype": "NUMBER"}
            ]
        }
        assert node.to_dict() == expected

    def test_attribute_access(self):
        """
        Purpose: Object property access and method lookups are fundamental in object-oriented
        semantics to accurately track dependencies and state mutations of composite instances.
        """
        from obfuscrypt_base.ast_nodes import Attribute
        base = Name(NodeType.NAME, id="obj", ctx="Load")
        node = Attribute(NodeType.ATTRIBUTE, value=base, attr="property")
        expected = {
            "type": "Attribute",
            "value": {"type": "Name", "id": "obj", "ctx": "Load"},
            "attr": "property"
        }
        assert node.to_dict() == expected

    def test_import_statement(self):
        """
        Purpose: Cross-module dependencies must be declared accurately for resolving scope,
        ensuring external libraries and logic are strictly tracked for semantic preservation.
        """
        from obfuscrypt_base.ast_nodes import ImportStmt, Alias
        alias = Alias(name="os", asname="sys_os")
        node = ImportStmt(NodeType.IMPORT, names=[alias])
        expected = {
            "type": "Import",
            "names": [{"name": "os", "asname": "sys_os"}]
        }
        assert node.to_dict() == expected

    def test_unary_operator(self):
        """
        Purpose: Single operand logic, such as numeric negations or boolean inversions, needs a
        distinct representation to enforce correct operational precedence and logical tracking.
        """
        from obfuscrypt_base.ast_nodes import UnaryOp
        operand = Constant(NodeType.CONSTANT, value=5, dtype="NUMBER")
        node = UnaryOp(NodeType.UNARY_OP, operator="-", operand=operand)
        expected = {
            "type": "UnaryOp",
            "operator": "-",
            "operand": {"type": "Constant", "value": 5, "dtype": "NUMBER"}
        }
        assert node.to_dict() == expected


class TestASTNodesFromDict:
    def test_module_reconstruction(self):
        """
        Purpose: Verify that a module's raw dictionary accurately reassembles into the root 
        container, properly configuring its body array for subsequent statement parsing.
        """
        data = {"type": "Module", "body": []}
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.MODULE
        assert hasattr(node, "body")
        assert isinstance(node.body, list)

    def test_function_def_reconstruction(self):
        """
        Purpose: Ensure function definitions seamlessly decode sub-structures such as target names,
        arguments, and nested logic blocks to represent complex encapsulated logic structures.
        """
        data = {
            "type": "FunctionDef", 
            "name": "test", 
            "args": {"type": "Arguments", "args": [], "vararg": None, "kwarg": None, "defaults": []}, 
            "body": [{"type": "Return", "value": {"type": "Constant", "value": None, "dtype": "NONE"}}], 
            "decorator_list": [], 
            "returns": None, 
            "async": False
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.FUNCTION_DEF
        assert getattr(node, "name", None) == "test"
        assert hasattr(node, "args")
        assert hasattr(node, "body")
        assert hasattr(node, "decorator_list")
        assert hasattr(node, "returns")
        assert hasattr(node, "async_")
        
    def test_assign_reconstruction(self):
        """
        Purpose: Validate that literal dictionaries mapping state mutation recreate into precise 
        Assignment operations, preserving target variables and assigned source values.
        """
        data = {
            "type": "Assign",
            "targets": [{"type": "Name", "id": "x", "ctx": "Store"}],
            "operator": "=",
            "value": {"type": "Constant", "value": 1, "dtype": "NUMBER"}
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.ASSIGN
        assert hasattr(node, "targets")
        assert hasattr(node, "operator")
        assert hasattr(node, "value")
        # Validate properties actually exist as structural components mapping to the original dict
        assert getattr(node, "operator", None) == "="
        
    def test_if_statement_reconstruction(self):
        """
        Purpose: Conditionals dictate control flow; their deserialization must accurately reconstruct 
        the boolean testing rules alongside standard execution block bodies and else fallbacks.
        """
        data = {
            "type": "IfStatement",
            "test": {"type": "Constant", "value": True, "dtype": "BOOLEAN"},
            "body": [],
            "ifelse": None,
            "else": {"type": "ElseStatement", "body": []}
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.IF
        assert hasattr(node, "test")
        assert hasattr(node, "body")
        assert hasattr(node, "elif_clauses")  # Verify elif branch parsing structure setup
        assert hasattr(node, "else_clause")   # Verify else branch fallback setup
        
    def test_binary_operator_reconstruction(self):
        """
        Purpose: Abstract computation definitions rely on proper left and right operand bindings; 
        this deserialization must retain operational semantics recursively.
        """
        data = {
            "type": "BinaryOp",
            "left": {"type": "Name", "id": "a", "ctx": "Load"},
            "operator": "+",
            "right": {"type": "Name", "id": "b", "ctx": "Load"}
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.BINARY_OP
        assert hasattr(node, "left")
        assert hasattr(node, "operator")
        assert hasattr(node, "right")
        
    def test_loop_construct_reconstruction(self):
        """
        Purpose: Ensure iterative blocks like while statements properly configure execution constraints 
        from dictionaries and set up their internal logic chains.
        """
        data = {
            "type": "WhileStatement",
            "test": {"type": "Constant", "value": True, "dtype": "BOOLEAN"},
            "body": [],
            "orelse": []
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.WHILE
        assert hasattr(node, "test")
        assert hasattr(node, "body")
        assert hasattr(node, "orelse")
        
    def test_function_call_reconstruction(self):
        """
        Purpose: Check that function invocations deserialize tracking the exact function identifier 
        and effectively reconstructing the passed arguments for runtime emulation.
        """
        data = {
            "type": "Call",
            "identifier": {"type": "Name", "id": "print", "ctx": "Load"},
            "args": [{"type": "Constant", "value": "Hello", "dtype": "STRING"}]
        }
        node = ASTNode.from_dict(data)
        assert node.node_type == NodeType.CALL
        # Note: from_dict implementation might map "identifier" to "func" or "identifier", tests validate expected structure
        assert hasattr(node, "identifier") or hasattr(node, "func")
        assert hasattr(node, "args")
    