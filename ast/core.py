class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions  # should be a list of functionDefinition

    def __repr__(self):
        return 'Program <%s> % functions'


class FunctionDefinition(ASTNode):
    def __init__(self, ret_type, name, body):
        # At some point this should also get a parameters field
        self.ret_type = ret_type
        self.body = body
        self.name = name

    def __repr__(self):
        return 'FunctionDef <type: %s, name:%s, body_id: %i>' % \
               (self.ret_type, self.name, id(self.body))


class MultiNode(ASTNode):
    def __init__(self, nodes, name):
        """This class accepts a list of nodes "nodes" and instatiates a MetaNode"""
        self.nodes = nodes  # list of statements
        self.name = "MultiNode :" + name


class ScopeBlock(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # list of statements

    def __repr__(self):
        return "ScopeBlock <id: %i, body_id:%i>" % (id(self), id(self.statements))


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


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class ExplicitConstant(ASTNode):
    def __init__(self, value, type_):
        # At some point this should also have 'Data type field'
        self.value = value
        self.type = type_


class Return(ASTNode):
    def __init__(self):
        # Only hadling void returns for now
        pass


class IfStatement(ASTNode):
    def __init__(self, expression, body, elsebody=None):
        self.expression = expression
        self.body = body
        self.elsebody = elsebody


class WhileStatement(ASTNode):
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block


class SwitchStatement(ASTNode):
    def __init__(self, expression, cases, default=None):
        self.expression = expression
        self.cases = cases
        self.default = default


class CaseStatement(ASTNode):
    def __init__(self, switch_expr, expression, statements):
        self.switch_expr = switch_expr
        self.expression = expression
        self.statements = statements


class BreakStatement(ASTNode):
    def __init__(self):
        pass

    def __repr__(self):
        return "Break"


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class ASTPrinter(NodeVisitor):
    pass  # Implement me
