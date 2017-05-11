from ast.core import NodeVisitor, ExplicitConstant
from graphviz import Digraph


class Visualizer(NodeVisitor):
    def __init__(self, parser):
        self.graph = Digraph(comment="The Round Table")
        self.parser = parser

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

        self.graph.edge(node_id, b_id)
        return node_id

    def visit_BinOp(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.op.value)
        left_id = self.visit(node.left)
        right_id = self.visit(node.right)
        self.graph.edge(node_id, left_id)
        self.graph.edge(node_id, right_id)
        return node_id
    def visit_UnaryOp(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.op.value)
        exp_id = self.visit(node.expression)
        self.graph.edge(node_id, exp_id)
        return node_id


    def visit_Return(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "Return void")

        return node_id

    def visit_Variable(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "Var <%s>" %node.name)
        return node_id

    def visit_VariableAssignment(self,node):
        node_id = str(id(node))
        self.graph.node(node_id,"Assign <%s>"%node.name)
        val_id = self.visit(node.value)
        self.graph.edge(node_id,val_id)
        return node_id

    def visit_VariableDeclaration(self,node):
        node_id = str(id(node))
        self.graph.node(node_id, "Decl %s %s"%(node.dtype, node.name))
        return node_id

    def visit_MultiNode(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, 'MultiNode')
        children = []
        for node in node.nodes:
            children.append(self.visit(node))
        for child in children:
            self.graph.edge(node_id, child)
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

    def visit_ExplicitConstant(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, str(node.value))

        return node_id

    def visit_IfStatement(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, 'IF')
        expr = self.visit(node.expression)
        bod = self.visit(node.body)
        else_bod = None
        if node.elsebody is not None:
            else_bod = self.visit(node.elsebody)

        self.graph.edge(node_id, expr)
        self.graph.edge(node_id, bod)
        if else_bod is not None:
            self.graph.edge(node_id, else_bod)
        return node_id

    def visit_WhileStatement(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "WHILE")
        expr = node.expression
        block = node.block

        expr_id = self.visit(expr)
        block_id = self.visit(block)

        self.graph.edge(node_id, expr_id)
        self.graph.edge(node_id, block_id)

        return node_id

    def visit_BreakStatement(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "BREAK")
        return node_id

    def visit_MultiNode(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, node.name)
        sub_nodes = []
        for sub_node in node.nodes:
            sub_nodes.append(self.visit(sub_node))

        for sub_node in sub_nodes:
            self.graph.edge(node_id, sub_node)

        return node_id

    def visit_SwitchStatement(self, node):

        node_id = str(id(node))

        self.graph.node(node_id, "switch")
        expr_id = self.visit(node.expression)
        self.graph.edge(node_id, expr_id)
        cases_id = self.visit(node.cases)
        self.graph.edge(node_id, cases_id)
        if node.default is not None:
            default_id = self.visit(node.default)
            self.graph.edge(node_id, default_id)

        return node_id

    def visit_CaseStatement(self, node):
        node_id = str(id(node))
        self.graph.node(node_id, "case")

        switch_expr_id = self.visit(node.switch_expr)
        self.graph.edge(node_id, switch_expr_id)

        expression_id = self.visit(node.expression)
        self.graph.edge(node_id,expression_id)
        statements_id = self.visit(node.statements)
        self.graph.edge(node_id,statements_id)
        return node_id

    def visit_ConstantString(self, node):
        node_id = str(id(node))
        self.graph.node(node_id,'"'+node.string+'"')

        return node_id

    def visualize(self):
        self.visit(self.parser.parse())
        self.graph.render('test-output/round-table.gv', view=True)
