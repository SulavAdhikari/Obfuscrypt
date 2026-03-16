from typing import Any, List, Dict
from obfuscrypt_base.ast_nodes import ASTNode, NodeType

class ASTObject:
    """Represents an object in the abstract syntax tree (AST) object tree"""
    def __init__(self, ASTNode_instance: 'ASTNode', parent_node=None, depth: int=0):
        self.ASTNode = ASTNode_instance
        self.depth = depth
        self.parent_node = parent_node
        self.child_nodes = self.get_child_nodes_from_body()
        self.child_statements = self.get_child_statements()
        self.variables = self.gather_variables()

    def gather_variables(self):
        """
        Recursively gathers all variables defined in the AST
        including their depth in the AST (Functions as scope of the variable)
        """
        variables = []
        if self.is_definition_node():
            if hasattr(self.ASTNode, "name"):
                variables.append({"name": self.ASTNode.name, "depth": self.depth})
            elif self.ASTNode.node_type == NodeType.ASSIGN:
                for target in getattr(self.ASTNode, "targets", []):
                    if hasattr(target, "id"):
                        variables.append({"name": target.id, "depth": self.depth})
        for child_node in self.child_nodes:
            variables.extend(child_node.gather_variables())
        return variables

    def get_child_nodes_from_body(self):
        """
        Gets all child nodes from the body of the AST node
        """
        child_objects = []
        if hasattr(self.ASTNode, "body") and self.ASTNode.body:
            for child_node in self.ASTNode.body:
                child_obj = ASTObject(child_node, parent_node=self, depth=self.depth + 1)
                child_objects.append(child_obj)
        return child_objects
    
    def get_child_statements(self):
        """
        Gets all child statements from the AST node
        """
        child_statements = []
        for child_node in self.child_nodes:
            if child_node.is_statement_node():
                child_statements.append(child_node)
        return child_statements

    def is_state_mutation_node(self):
        """
        Checks if the node is a state mutation node
        i.e. it mutates the state of the program variables
        """
        if self.ASTNode.node_type in [NodeType.ASSIGN]:
            return True
        return False

    def is_control_flow_node(self):
        if self.ASTNode.node_type in [
            NodeType.IF,
            NodeType.ELIF,
            NodeType.ELSE,
            NodeType.RETURN,
            NodeType.BREAK,
            NodeType.CONTINUE,
            NodeType.WHILE,
            NodeType.FOR,
            NodeType.TRY,
            NodeType.WITH,
            NodeType.RAISE,
            ]:
            return True
        return False

    def is_statement_node(self):
        """
        Checks if the node is a statement node
        """
        if getattr(self.ASTNode, "is_statement_node", False):
            return True
        return False

    def is_definition_node(self):
        """
        Checks if the node is a definition node
        i.e. it defines a new variable, function, or class
        """
        if self.ASTNode.node_type in [NodeType.FUNCTION_DEF, NodeType.CLASS_DEF]:
            return True
        if self.ASTNode.node_type in [NodeType.ASSIGN]:
            return True
        return False

    def is_import_node(self):
        """
        Checks if the node is an import node
        i.e. it imports a module or package
        """
        if self.ASTNode.node_type in [NodeType.IMPORT, NodeType.IMPORT_FROM]:
            return True
        return False

    def is_call_node(self):
        """
        Checks if the node is a call node
        i.e. it calls a function or method
        """
        if self.ASTNode.node_type in [NodeType.CALL]:
            return True
        return False

    def has_body(self):
        """
        Checks if the node has a body
        i.e. it has a list of statements to execute (eg. function body or if block body)
        """
        if hasattr(self.ASTNode, "body"):
            return True
        return False
    
    def has_name(self):
        if hasattr(self.ASTNode, "name"):
            return True
        return False

    @property
    def distance_from_main_module(self):
        """
        Returns the distance of the node from the main module
        main module has depth 0 and its first level children have an incremented depth and so on. 
        """
        return self.depth

    def increment_depth(self):
        self.depth += 1