from ast.core import NodeVisitor, ExplicitConstant
from graphviz import Digraph


class Visualizer(NodeVisitor):
    def __init__(self):
        self.graph = Digraph(comment="The Round Table")

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_FunctionCall(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.callee_name)
        params = []
        for param in node.parameters:
            params.append(self.visit(param))
        for n_id in params:
            self.graph.edge(node_id, n_id)

        return node_id

    def visit_NoOperation(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.__repr__())

        return node_id

    def visit_ScopeBlock(self, node):
        # later scoping will be handled here as well
        node_id = str(id(node))

        self.graph.node(node_id, "Scope block")
        statements = []
        for statement in node.statements:
            statements.append(self.visit(statement))

        for s_id in statements:
            self.graph.edge(node_id, s_id)
        return node_id

    def visit_FunctionDefinition(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.name)

        b_id = self.visit(node.body)

        self.graph.edge(node_id,b_id)
        return node_id

    def visit_Return(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "Return void")

        return node_id

    def visit_Program(self, node):
        # remove extern printf when the Symbol Resource Table Arrives

        node_id = str(id(node))

        self.graph.node(node_id, "PROGRAM");
        functions = []

        for func in node.functions:
            functions.append(self.visit(func))

        for func_id in functions:
            self.graph.edge(node_id, func_id)
        return node_id
    def visit_ExplicitConstant(self,node):
        node_id = str(id(node))
        self.graph.node(node_id, str(node.value))

        return node_id
    def run(self,node):
        self.visit(node)
        self.graph.render('test-output/round-table.gv',view=True)
