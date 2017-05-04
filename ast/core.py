class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions # should be a list of functionDefinition

    def __repr__(self):
        return 'Program <%s> % functions'


class FunctionDefinition(ASTNode):
    def __init__(self, ret_type, name, body):
        # At some point this should also get a parameters field
        self.ret_type = ret_type
        self.body = body
        self.name = name

    def __repr__(self):
        return 'FunctionDef <type: %s, name:%s, body_id: %i>'%\
               (self.ret_type, self.name, id(self.body))


class MultiNode(ASTNode):
    def __init__(self, nodes):
        self.nodes = nodes    # list of statements


class ScopeBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements    # list of statements

    def __repr__(self):
        return "ScopeBlock <id: %i, body_id:%i>" %(id(self), id(self.statements))


class NoOperation(ASTNode):
    def __init__(self):
        """This represents an empty statement"""
        pass

    def __repr__(self):
        return "NoOperation"


class FunctionCall(ASTNode):
    def __init__(self, callee_name, parameters):
        self.callee_name = callee_name
        self.parameters = parameters


class ExplicitConstant(ASTNode):
    def __init__(self, value, type_):
        # At some point this should also have 'Data type field'
        self.value = value
        self.type = type_


class Return(ASTNode):
    def __init__(self):
        # Only hadling void returns for now
        pass


class VariableDeclaration(ASTNode):
    def __init__(self, name, d_type):
        self.name = name
        self.type = d_type


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class VariableAssignment(ASTNode):
    def __init__(self, name, value):
        self.value = value
        self.name = name

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class ASTPrinter(NodeVisitor):
   pass # Implement me