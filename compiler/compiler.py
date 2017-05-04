from ast.core import NodeVisitor, ExplicitConstant, WhileStatement
from tokens import INT


class LoopSwitchStack:
    def __init__(self):
        self._scopes = []

    def add_item(self, scope):
        assert (isinstance(scope, WhileStatement))
        self._scopes.append(scope)

    def exit_item(self, scope):
        # 'eat' scope
        assert (self._scopes[-1] == scope)
        self._scopes.pop()

    def get_top_loop_switch(self):
        if len(self._scopes) == 0:
            raise Exception("None valid syntax")
        else:
            return self._scopes[-1]


class Compiler(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.stack_pos = 0  # This will become an object later
        self.loop_switch_stack = LoopSwitchStack()

    def compile(self):
        head = self.parser.parse()
        return self.visit(head)

    def visit_FunctionCall(self, node):
        code = ""
        old_stack_pos = self.stack_pos
        for parameter in node.parameters[::-1]:
            code += self.visit(parameter)

        code += "call %s\n" % ("_" + node.callee_name)
        code += "add esp, %i\n" % (self.stack_pos - old_stack_pos)
        self.stack_pos = old_stack_pos
        return code

    def visit_NoOperation(self, node):
        return ""

    def visit_ScopeBlock(self, node):
        # later scoping will be handled here as well
        code = ""
        for statement in node.statements:
            code += self.visit(statement)
        return code

    def visit_MultiNode(self, node):
        code = ""
        for sub_node in node.nodes:
            code += self.visit(sub_node)
        return code

    def visit_FunctionDefinition(self, node):
        # TODO!!!! function declarations should have a jump to right after the body to
        # handle nested functions correctly
        code = "_%s: \n" % node.name
        code += """push ebp
mov ebp, esp\n"""
        code += self.visit(node.body)
        code += "pop ebp\nret\n"
        return code

    def visit_Return(self, node):
        return "pop ebp\nret\n"

    def visit_Program(self, node):
        # remove extern printf when the Symbol Resource Table Arrives
        code = """"global _main
extern _printf
section .text\n"""
        for func in node.functions:
            code += self.visit(func)
        return code

    def visit_ExplicitConstant(self, node):

        if node.type == INT:
            self.stack_pos += 4
            return "push %i\n" % (node.value)

    def visit_WhileStatement(self, node):
        self.loop_switch_stack.add_item(node)
        start_label = '__while_label_start' + str(id(node))
        end_label = '__while_label_end' + str(id(node))

        code = start_label + ':\n'
        code += self.visit(node.expression)
        code += "pop eax\ncmp eax,0\n"
        code += "jz " + end_label + '\n'
        code += self.visit(node.block)
        code += "\njmp " + start_label + '\n'
        code += end_label + ":\n"
        self.loop_switch_stack.exit_item(node)
        return code

    def visit_BreakStatement(self,node):
        code = "jmp __while_label_end"+str(id(self.loop_switch_stack.get_top_loop_switch()))+":\n"
        return code
